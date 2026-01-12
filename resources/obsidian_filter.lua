-- obsidian_filter.lua
-- Simplified for stability

function BlockQuote(el)
  local first_block = el.content[1]
  if first_block and first_block.t == "Para" then
    -- We need to check if this is a callout by looking at the start
    -- But we want to preserve the REST of the inlines for the title
    
    local inlines = first_block.content
    local tag = nil
    local title_start_index = 0
    local env = "noteblock"
    
    -- Heuristic: stringify the first few nodes to check for Pattern
    -- usually: Str(>), Space, Str([!INFO]) OR Str([!INFO])
    -- Let's try to stringify the whole first block just to detecting the TYPE
    -- Then we locate where to split.
    
    local text = pandoc.utils.stringify(first_block)
    local match_tag, match_title_str = text:match("^%s*>?%s*%[!([%w_-]+)%]%s*(.*)")
    
    if match_tag then
        tag = match_tag:upper()
        if tag == "TIP" then env = "tipblock"
        elseif tag == "WARNING" then env = "warningblock"
        elseif tag == "IMPORTANT" then env = "importantblock"
        elseif tag == "CAUTION" or tag == "DANGER" then env = "cautionblock"
        elseif tag == "ANALOGY" then env = "analogyblock"
        end

        -- Find the split point in 'inlines'
        -- We want to skip the "[!TAG]" part and any preceding ">"
        -- This is tricky to do perfectly with nodes, so we'll scan.
        -- We look for the node containing "[!TAG]"
        
        for i, node in ipairs(inlines) do
            if node.t == "Str" and node.text:find("%[!%w+%]?") then
                title_start_index = i + 1
                break
            elseif node.t == "Str" and node.text:find("%[!%w+") then
                 -- Split across nodes? Unlikely but possible.
                 -- Assume simple case: "[!INFO]" is one node or "[!","INFO","]"
            end
            -- handle split tag "[!", "INFO", "]"?
            if node.t == "Str" and node.text == "[!" then
                -- check next?
                title_start_index = i + 1 -- naive
            end
        end
        
        -- Fallback: if we couldn't pinpoint, assume text match was correct and title is match_title_string
        -- BUT we want rich text. 
        -- Alternative: Re-parse the "text" variable? No, we lose bold/math.
        
        -- Robust Approach:
        -- Locate the node that has the Tag.
        -- If we can't find it easily, we might just assume it's the first few nodes.
        -- "[!TAG]" is usually 1 Str node if no spaces inside.
        
        local title_inlines = {}
        local body_inlines = {}
        local found_tag = false
        local collecting_body = false
        
        for i, node in ipairs(inlines) do
            if collecting_body then
                table.insert(body_inlines, node)
            elseif not found_tag then
                local s = pandoc.utils.stringify(node)
                if s:find("%[!%w+.*%]") then
                    found_tag = true
                elseif s:find("%]%s*$") and i > 1 then 
                    -- maybe end of tag
                    found_tag = true
                end
            else
                -- Found tag, checking for break to end title
                if node.t == "SoftBreak" or node.t == "LineBreak" then
                    collecting_body = true
                    -- Don't add the break to title
                else
                    table.insert(title_inlines, node)
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

        local box_title_tex = ""
        
        if #title_inlines == 0 then
            -- Default Title
             box_title_tex = tag:sub(1,1)..tag:sub(2):lower()
        else
            -- Convert title_inlines to LaTeX
            -- Use pandoc.write if available (Pandoc 2.0+)
            if pandoc.write then
                local doc = pandoc.Pandoc({pandoc.Plain(title_inlines)})
                box_title_tex = pandoc.write(doc, "latex")
                -- Strip potentially surrounding whitespace
                box_title_tex = box_title_tex:gsub("^%s+", ""):gsub("%s+$", "")
            else
                -- Fallback: Manual serialization
                for _, node in ipairs(title_inlines) do
                    if node.t == "Str" then box_title_tex = box_title_tex .. node.text:gsub("[%%&%$#_{}~]", "\\%1")
                    elseif node.t == "Space" then box_title_tex = box_title_tex .. " "
                    elseif node.t == "Math" then box_title_tex = box_title_tex .. "$" .. node.text .. "$"
                    elseif node.t == "Strong" then box_title_tex = box_title_tex .. "\\textbf{" .. pandoc.utils.stringify(node) .. "}"
                    elseif node.t == "Emph" then box_title_tex = box_title_tex .. "\\emph{" .. pandoc.utils.stringify(node) .. "}"
                    else box_title_tex = box_title_tex .. pandoc.utils.stringify(node)
                    end
                end
            end
        end
        
        -- Construct the box
        local blocks = {}
        table.insert(blocks, pandoc.RawBlock("latex", "\\begin{" .. env .. "}{" .. box_title_tex .. "}"))
        
        if #body_inlines > 0 then
            table.insert(blocks, pandoc.Para(body_inlines))
        end
        
        for i = 2, #el.content do
            table.insert(blocks, el.content[i])
        end
        table.insert(blocks, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))
        
        return blocks
    end
  end
end

function Span(el)
  if el.classes:includes("mark") then
    local new_content = {pandoc.RawInline("latex", "\\hl{")}
    for _, item in ipairs(el.content) do
      table.insert(new_content, item)
    end
    table.insert(new_content, pandoc.RawInline("latex", "}"))
    return new_content
  end
end

function Link(el)
  if el.classes:includes("wikilink") then
    local target = el.target
    
    -- Clean the target to match build_book.py logic (remove leading numbers/punctuation)
    -- Regex equivalent to ^[\d\s\.\-_]+(.*)
    local clean_target = target:match("^[%d%s%.%-_]*(.*)") or target
    
    local target_id = clean_target:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
    local content = el.content
    
    -- If content is empty or matches the raw target (default behavior), use clean_target
    local content_text = pandoc.utils.stringify(content)
    if #content == 0 or content_text == target then
        content = {pandoc.Str(clean_target)}
    end
    
    return pandoc.Link(content, "#" .. target_id)
  end
end

-- Global vars to store config
local config_max_width = nil
local config_max_height = nil

function Meta(m)
    io.stderr:write("Meta function called.\n")
    for k, v in pairs(m) do
        io.stderr:write("Meta key: " .. k .. "\n")
    end

    if m["image-max-width"] then
        config_max_width = pandoc.utils.stringify(m["image-max-width"])
        io.stderr:write("Meta: Found max_width = " .. config_max_width .. "\n")
    end
    if m["image-max-height"] then
        config_max_height = pandoc.utils.stringify(m["image-max-height"])
        io.stderr:write("Meta: Found max_height = " .. config_max_height .. "\n")
    end
    return m
end

-- Helper to check if block contains only one image (ignoring whitespace)
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

-- Function to generate LaTeX Figure
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
             size_opts = "max width=0.9\\linewidth,keepaspectratio" -- Ultimate fallback
        end
    end

    -- Caption handling
    local caption_text = pandoc.utils.stringify(img.caption)
    local caption_tex = ""
    if #caption_text > 0 and caption_text ~= "fig:" and caption_text ~= "\\" then -- Filter out dummy captions
        caption_tex = "\\caption{" .. caption_text .. "}"
    end

    -- Fix path: Pandoc may URL-encode the src (e.g. %20 for space). LaTeX needs the real path.
    local src_path = img.src:gsub("%%20", " ")

    -- Construct LaTeX
    local latex = "\\begin{figure}[H]\n\\centering\n\\includegraphics[" .. size_opts .. "]{" .. src_path .. "}\n" .. caption_tex .. "\n\\end{figure}"
    
    return pandoc.RawBlock("latex", latex)
end

function Para(el)
    local img = get_standalone_image(el)
    if img then
        return create_latex_figure(img)
    end
    return el
end

function Image(el)
  -- Remove wikilink class if present
  if el.classes:includes("wikilink") then
      el.classes = el.classes:filter(function(c) return c ~= "wikilink" end)
  end
  -- Inline images (not standalone) are left to default handling or stripped of specific classes
  return el
end

function Str(el)
  if el.text == "☐" then
     return pandoc.RawInline("latex", "$\\square$")
  elseif el.text == "☒" then
     return pandoc.RawInline("latex", "$\\boxtimes$")
  end
end

-- Math Fix: Replace \ce{...} with \mathrm{...}
function Math(el)
    if el.text:find("\\ce{") then
        -- Simple global substitution for \ce to \mathrm
        -- This preserves the braces structure: \ce{...} -> \mathrm{...}
        -- Assuming \ce only takes one argument block.
        local new_tex = el.text:gsub("\\ce", "\\symup")
        el.text = new_tex
        return el
    end
end

-- Fix Table Overflow: Force wrapping for tables with default (0) width
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
         -- Add a buffer (e.g., 3 chars) to help short words get more weight
         return #pandoc.utils.stringify(cell) + 10
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
    -- (e.g. sqrt(10)=3.1 vs sqrt(100)=10 is 1:3 ratio, whereas 10:100 is 1:10)
    
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
         
         spec[2] = percent * 0.98 -- Scale to 98% of page
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

