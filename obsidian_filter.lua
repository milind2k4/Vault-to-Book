-- obsidian_filter.lua
-- Simplified for stability

function BlockQuote(el)
  local first_block = el.content[1]
  if first_block and first_block.t == "Para" then
    local text_content = ""
    -- Reconstruct text from Para
    for _, inline in ipairs(first_block.content) do
       if inline.t == "Str" or inline.t == "Space" then
          text_content = text_content .. (inline.text or " ")
       end
    end

    local type, title = text_content:match("%[!([%w_-]+)%]%s*(.*)")
    
    if type then
      -- Fallback: Use standard BlockQuote but bold the title
      -- This avoids dependencies on awesomebox
      
      local new_blocks = {}
      
      if title and title ~= "" then
         table.insert(new_blocks, pandoc.Para({pandoc.Strong(pandoc.Str(title:upper()))}))
      end
      
      -- Add content (keeping the raw text including [!NOTE] for now as cleaning is complex, 
      -- or we can attempt to clean strict [!NOTE] prefix)
      
      -- Clean the first block?
      -- Let's just dump content for now.
      for _, b in ipairs(el.content) do
          table.insert(new_blocks, b)
      end
      
      return pandoc.BlockQuote(new_blocks)
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
