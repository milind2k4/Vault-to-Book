---@diagnostic disable: undefined-global
-- obsidian_filter.lua
-- Pandoc Lua filter to process Obsidian-specific syntax for LaTeX export.
-- Handles callouts, wikilinks, image sizing/placement, equations, and tables.

--- Handles Obsidian Callouts (BlockQuotes).
-- Converts citation-style blockquotes `> [!INFO]` into LaTeX environments.
-- Supported tags: TIP, WARNING, IMPORTANT, CAUTION, DANGER, ANALOGY.
-- @param el The BlockQuote element.
function BlockQuote(el)
    local first_block = el.content[1]
    if first_block and first_block.t == "Para" then
        local inlines = first_block.content

        -- Stringify first block to see if it looks like a callout
        local text = pandoc.utils.stringify(first_block)
        local match_tag, match_title_str = text:match("^%s*>?%s*%[!([%w_-]+)%]%s*(.*)")

        if match_tag then
            local tag = match_tag:upper()
            local env = "noteblock"

            -- Map tags to environments
            local env_map = {
                TIP = "tipblock",
                WARNING = "warningblock",
                IMPORTANT = "importantblock",
                CAUTION = "cautionblock",
                DANGER = "cautionblock",
                ANALOGY = "analogyblock"
            }
            if env_map[tag] then env = env_map[tag] end

            -- Extract Title Inlines
            -- iterate inlines, skip until we pass the "[!TAG]" pattern
            local title_inlines = {}
            local body_inlines = {}
            local found_tag_end = false
            local collecting_body = false

            for i, node in ipairs(inlines) do
                if collecting_body then
                    table.insert(body_inlines, node)
                elseif found_tag_end then
                    if node.t == "SoftBreak" or node.t == "LineBreak" then
                        collecting_body = true
                    else
                        table.insert(title_inlines, node)
                    end
                else
                    if node.t == "Str" then
                        -- Check for full tag "[!INFO]"
                        if node.text:find("%[!%w+.*%]") then
                            found_tag_end = true
                            -- If text remains after tag, keep it
                            local s = node.text:gsub("^%s*>?%s*%[!%w+.-%]%s*", "")
                            if s ~= "" then
                                table.insert(title_inlines, pandoc.Str(s))
                            end
                        elseif node.text:find("%]") and i > 1 then
                            -- Handle split tag case: "[!", "INFO", "]"
                            -- If we hit "]", assume it's the end of the split tag
                            found_tag_end = true
                        end
                    elseif node.t == "Space" or node.t == "SoftBreak" then
                        -- Skip spaces before/inside tag
                    end
                end
            end

            -- Clean leading ">", ":", or whitespace from title_inlines
            local clean = false
            while not clean and #title_inlines > 0 do
                local first = title_inlines[1]
                if first.t == "Space" or first.t == "SoftBreak" then
                    table.remove(title_inlines, 1)
                elseif first.t == "Str" then
                    -- Check for leading ">" or ":"
                    local s = first.text
                    local new_s = s:gsub("^%s*[>:]+%s*", "")
                    if new_s == "" then
                        -- Node became empty, remove it
                        table.remove(title_inlines, 1)
                    else
                        -- Node partially cleaned, update and stop
                        first.text = new_s
                        clean = true
                    end
                else
                    -- Other elements (Emph, Strong), stop cleaning
                    clean = true
                end
            end

            -- Generate Title LaTeX
            local box_title_tex = ""
            if #title_inlines == 0 then
                -- Default Title matches tag name (Capitalized)
                box_title_tex = tag:sub(1, 1) .. tag:sub(2):lower()
            else
                if pandoc.write then
                    local doc = pandoc.Pandoc({ pandoc.Plain(title_inlines) })
                    box_title_tex = pandoc.write(doc, "latex")
                    box_title_tex = box_title_tex:gsub("^%s+", ""):gsub("%s+$", "")
                else
                    -- Fallback manual serialization
                    box_title_tex = match_title_str or tag
                end
            end

            -- Construct LaTeX Block
            local blocks = {}
            table.insert(blocks, pandoc.RawBlock("latex", "\\begin{" .. env .. "}{" .. box_title_tex .. "}"))

            -- Add body inlines from the first block if any
            if #body_inlines > 0 then
                table.insert(blocks, pandoc.Para(body_inlines))
            end

            -- Add remaining blocks (body of the blockquote)
            for i = 2, #el.content do
                table.insert(blocks, el.content[i])
            end
            table.insert(blocks, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))

            return blocks
        end
    end
end

--- Wraps text marked with `==text==` (mark class) in LaTeX `\hl{}`.
-- @param el The Span element.
function Span(el)
    if el.classes:includes("mark") then
        local new_content = { pandoc.RawInline("latex", "\\hl{") }
        for _, item in ipairs(el.content) do
            table.insert(new_content, item)
        end
        table.insert(new_content, pandoc.RawInline("latex", "}"))
        return new_content
    end
end

--- Converts Wikilinks `[[Target]]` to internal links `\ref{target-id}` or similar.
-- Cleans the target ID to match the slugification used in `builder.py`.
-- @param el The Link element.
function Link(el)
    if el.classes:includes("wikilink") then
        local target = el.target

        -- Clean the target to match build_book.py logic (remove leading numbers/punctuation)
        local clean_target = target:match("^[%d%s%.%-_]*(.*)") or target

        local target_id = clean_target:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
        local content = el.content

        -- If content is empty or matches the raw target (default behavior), use clean_target
        local content_text = pandoc.utils.stringify(content)
        if #content == 0 or content_text == target then
            content = { pandoc.Str(clean_target) }
        end

        return pandoc.Link(content, "#" .. target_id)
    end
end

-- Global vars to store config
local config_max_width = nil
local config_max_height = nil

--- Captures global metadata passed from Pandoc.
-- Used to set global image max width/height configuration from `config.yaml`.
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
-- Used to decide if an image should be wrapped in a `figure` environment.
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
-- Handles sizing (max-width/height), captions, and placement `[H]`.
-- @param img The Image element.
local function create_latex_figure(img)
    local has_width = false
    local explicit_dim = ""

    -- Check for explicit dimensions from Obsidian syntax or attributes
    for k, v in pairs(img.attributes) do
        if k == "width" then
            has_width = true
            explicit_dim = explicit_dim .. "width=" .. v .. ","
        elseif k == "height" then
            has_width = true
            explicit_dim = explicit_dim .. "height=" .. v .. ","
        end
    end

    -- Determine Sizing
    local size_opts = ""
    if has_width then
        -- Apply explicit dimensions (and keep aspect ratio)
        size_opts = explicit_dim .. "keepaspectratio"
    else
        -- Apply global defaults
        local max_w = config_max_width
        local max_h = config_max_height

        -- Fallback to global metadata lookup if cache missed (safety)
        if not max_w and PANDOC_DOCUMENT and PANDOC_DOCUMENT.meta and PANDOC_DOCUMENT.meta["image-max-width"] then
            max_w = pandoc.utils.stringify(PANDOC_DOCUMENT.meta["image-max-width"])
        end
        if not max_h and PANDOC_DOCUMENT and PANDOC_DOCUMENT.meta and PANDOC_DOCUMENT.meta["image-max-height"] then
            max_h = pandoc.utils.stringify(PANDOC_DOCUMENT.meta["image-max-height"])
        end

        if max_h then
            -- Prioritize Max Height
            size_opts = "max height=" .. max_h .. ",keepaspectratio"
        elseif max_w then
            size_opts = "max width=" .. max_w .. ",keepaspectratio"
        else
            size_opts = "max width=0.9\\linewidth,keepaspectratio"  -- Ultimate fallback
        end
    end

    -- Caption handling
    local caption_text = pandoc.utils.stringify(img.caption)
    local caption_tex = ""
    -- Filter out dummy captions
    if #caption_text > 0 and caption_text ~= "fig:" and caption_text ~= "\\" then
        caption_tex = "\\caption{" .. caption_text .. "}"
    end

    -- Fix path: Pandoc may URL-encode the src (e.g. %20 for space). LaTeX needs the real path.
    local src_path = img.src:gsub("%%20", " ")

    -- Construct LaTeX
    local latex = "\\begin{figure}[H]\n\\centering\n\\includegraphics[" ..
    size_opts .. "]{" .. src_path .. "}\n" .. caption_tex .. "\n\\end{figure}"

    return pandoc.RawBlock("latex", latex)
end


--- Processes Paragraphs to detect and convert standalone images.
-- @param el The Para element.
function Para(el)
    local img = get_standalone_image(el)
    if img then
        return create_latex_figure(img)
    end
    return el
end

--- Cleans up inline images (removes wikilink class).
-- @param el The Image element.
function Image(el)
    -- Remove wikilink class if present
    if el.classes:includes("wikilink") then
        el.classes = el.classes:filter(function(c) return c ~= "wikilink" end)
    end
    -- Inline images (not standalone) are left to default handling or stripped of specific classes
    return el
end

--- Handles special characters like checkboxes.
-- @param el The Str element.
function Str(el)
    if el.text == "☐" then
        return pandoc.RawInline("latex", "$\\square$")
    elseif el.text == "☒" then
        return pandoc.RawInline("latex", "$\\boxtimes$")
    end
end

--- Fixes chemical equations by replacing `\ce{}` with `\symup{}` (or equivalent).
-- @param el The Math element.
function Math(el)
    if el.text:find("\\ce{") then
        local new_tex = el.text:gsub("\\ce", "\\symup")
        el.text = new_tex
        return el
    end
end

--- Adjusts table column widths using a square-root scaling algorithm.
-- Ensures that columns with more content get more space, but with diminishing returns.
-- Essential for preventing wide tables from overflowing the page.
-- @param el The Table element.
function Table(el)
    local colspecs = el.colspecs
    local needs_fix = false
    local count = #colspecs

    -- Smart Column Widths: Calculate based on content length
    -- 1. Scan header and body to find max char length per column
    local col_max_lens = {}
    for i = 1, count do col_max_lens[i] = 1 end -- Init with 1 to avoid div by zero

    -- Check Header
    local function get_cell_len(cell)
        -- Add a buffer (e.g., 4 chars) to help short words get more weight
        return #pandoc.utils.stringify(cell) + 4
    end

    if el.head then
        for _, row in ipairs(el.head.rows) do
            for i, cell in ipairs(row.cells) do
                if i <= count then
                    local len = get_cell_len(cell)
                    if len > col_max_lens[i] then col_max_lens[i] = len end
                end
            end
        end
    end

    -- Check Body (first 20 rows to save perf on huge tables)
    for _, body in ipairs(el.bodies) do
        for r_idx, row in ipairs(body.body) do
            if r_idx > 20 then break end
            for i, cell in ipairs(row.cells) do
                if i <= count then
                    local len = get_cell_len(cell)
                    if len > col_max_lens[i] then col_max_lens[i] = len end
                end
            end
        end
    end

    -- Assign Proportional Widths using Square Root Scaling
    -- This ensures short columns get relatively more space compared to linear scaling
    local total_weight = 0
    local weights = {}

    for i = 1, count do
        local w = math.sqrt(col_max_lens[i])
        weights[i] = w
        total_weight = total_weight + w
    end

    for i, spec in ipairs(colspecs) do
        local w = weights[i]
        local percent = w / total_weight

        -- Enforce min width of 12% to avoid squashing
        if percent < 0.12 and count <= 6 then percent = 0.12 end
        spec[2] = percent * 0.98  -- Scale to 98% of page
    end

    -- Re-normalize
    local final_total = 0
    for _, spec in ipairs(colspecs) do final_total = final_total + spec[2] end
    if final_total > 0.99 then
        local scale = 0.98 / final_total
        for _, spec in ipairs(colspecs) do spec[2] = spec[2] * scale end
    end

    el.colspecs = colspecs
    return el
end
