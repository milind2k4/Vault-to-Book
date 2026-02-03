-- images.lua
--[[
    Lua filter for handling image sizing, captions, and LaTeX Figure generation.

    Functions:
    - Captures global size configuration.
    - Detects standalone images.
    - Generates LaTeX `figure` environments with `[H]` placement.
    - Handles explicit resizing attributes (`width`, `height`).
]]

---@diagnostic disable: undefined-global

-- Configuration Defaults
local config_max_width = nil
local config_max_height = nil

--- Captures global metadata passed from Pandoc.
-- Sets global image configuration (max-width/height) from document metadata.
-- @param m The Meta map.
function Meta(m)
    if m["image-max-width"] then
        config_max_width = pandoc.utils.stringify(m["image-max-width"])
    end
    if m["image-max-height"] then
        config_max_height = pandoc.utils.stringify(m["image-max-height"])
    end
    return m
end

--- Checks if a block contains a single isolated image.
-- @param block The Block element (Para or Plain).
-- @return The Image element if standalone, nil otherwise.
local function get_standalone_image(block)
    if block.t ~= "Para" and block.t ~= "Plain" then return nil end
    local img = nil
    for _, elem in ipairs(block.content) do
        if elem.t == "Image" then
            if img then return nil end -- More than one image
            img = elem
        elseif elem.t ~= "Space" and elem.t ~= "SoftBreak" then
            return nil -- Contains non-whitespace text
        end
    end
    return img
end

--- Generates a LaTeX `figure` environment for an image.
-- Applies strict placement `[H]`, centering, and correct sizing options.
-- @param img The Image element.
local function create_latex_figure(img)
    local has_width = false
    local explicit_dim = ""

    -- Check for explicit dimensions
    for k, v in pairs(img.attributes) do
        if k == "width" then
            has_width = true
            explicit_dim = explicit_dim .. "width=" .. v .. ","
        elseif k == "height" then
            has_width = true
            explicit_dim = explicit_dim .. "height=" .. v .. ","
        end
    end

    -- Determine Sizing Options
    local size_opts = ""
    if has_width then
        size_opts = explicit_dim .. "keepaspectratio"
    else
        -- Logic: Defaults -> Metadata -> Fallback
        local max_w = config_max_width
        local max_h = config_max_height

        -- Late fallback to document metadata if globals aren't set
        if not max_w and PANDOC_DOCUMENT and PANDOC_DOCUMENT.meta and PANDOC_DOCUMENT.meta["image-max-width"] then
            max_w = pandoc.utils.stringify(PANDOC_DOCUMENT.meta["image-max-width"])
        end
        if not max_h and PANDOC_DOCUMENT and PANDOC_DOCUMENT.meta and PANDOC_DOCUMENT.meta["image-max-height"] then
            max_h = pandoc.utils.stringify(PANDOC_DOCUMENT.meta["image-max-height"])
        end

        if max_h then
            size_opts = "max height=" .. max_h .. ",keepaspectratio"
        elseif max_w then
            size_opts = "max width=" .. max_w .. ",keepaspectratio"
        else
            size_opts = "max width=0.9\\linewidth,keepaspectratio"
        end
    end

    -- Caption Processing
    local caption_text = pandoc.utils.stringify(img.caption)
    local caption_tex = ""
    if #caption_text > 0 and caption_text ~= "fig:" and caption_text ~= "\\" then
        caption_tex = "\\caption{" .. caption_text .. "}"
    end

    -- Fix Path (decode URI percent-encoding)
    local src_path = img.src:gsub("%%20", " ")

    -- Generate LaTeX Block
    local latex = "\\begin{figure}[H]\n\\centering\n\\includegraphics[" ..
        size_opts .. "]{" .. src_path .. "}\n" .. caption_tex .. "\n\\end{figure}"

    return pandoc.RawBlock("latex", latex)
end

--- Transforms standalone image paragraphs into LaTeX figures.
-- @param el The Para element.
function Para(el)
    local img = get_standalone_image(el)
    if img then
        return create_latex_figure(img)
    end
    return el
end

--- Cleanup for inline images.
-- Removes `wikilink` class from inline images.
-- @param el The Image element.
function Image(el)
    if el.classes:includes("wikilink") then
        el.classes = el.classes:filter(function(c) return c ~= "wikilink" end)
    end
    return el
end
