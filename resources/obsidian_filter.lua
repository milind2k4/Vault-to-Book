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
        local found_tag = false
        for i, node in ipairs(inlines) do
            if not found_tag then
                local s = pandoc.utils.stringify(node)
                if s:find("%[!%w+.*%]") then
                    found_tag = true
                elseif s:find("%]%s*$") and i > 1 then 
                    -- maybe end of tag
                    found_tag = true
                end
            else
                table.insert(title_inlines, node)
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

function Image(el)
  if el.classes:includes("wikilink") then
      el.classes = el.classes:filter(function(c) return c ~= "wikilink" end)
      return el
  end
end

function Str(el)
  if el.text == "☐" then
     return pandoc.RawInline("latex", "$\\square$")
  elseif el.text == "☒" then
     return pandoc.RawInline("latex", "$\\boxtimes$")
  end
end
