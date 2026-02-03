-- links.lua
-- Lua filter for converting Obsidian Wikilinks to standard LaTeX internal references.
--
-- Handles:
-- - [[Target]] -> \ref{target-id}
-- - [[Target|Alias]] -> Custom link text
-- - [[File#Heading]] -> Anchor references
--
-- Also cleans up target IDs to match slugification rules used by the build system.

---@diagnostic disable: undefined-global

--- Converts Wikilinks to internal LaTeX references.
-- Transforms `[[Target]]` syntax into Pandoc Link objects with sanitized IDs.
-- @param el The Link element.
function Link(el)
    if el.classes:includes("wikilink") then
        local target = el.target
        local file_part, anchor_part = target:match("^(.*)#(.*)$")
        local target_id = ""

        if anchor_part then
            -- Slugify specific heading/anchor
            anchor_part = anchor_part:match("^%s*(.-)%s*$")
            target_id = anchor_part:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
        else
            -- Slugify file target (stripping leading numbers/punctuation)
            local clean_target = target:match("^[%d%s%.%-_]*(.*)") or target
            target_id = clean_target:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
        end

        local content = el.content

        -- Generate clean display text if not already custom
        local clean_label = target:match("^[%d%s%.%-_]*(.*)") or target
        local content_text = pandoc.utils.stringify(content)

        -- Use cleaned label if content matches raw target (default auto-text) or is empty
        if #content == 0 or content_text == target then
            content = { pandoc.Str(clean_label) }
        end

        -- Create internal link with sanitized ID
        return pandoc.Link(content, "#" .. target_id)
    end
end
