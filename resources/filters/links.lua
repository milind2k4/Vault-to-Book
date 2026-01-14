---@diagnostic disable: undefined-global
-- links.lua
-- Converts Wikilinks `[[Target]]` to internal links `\ref{target-id}` or similar.

--- Converts Wikilinks `[[Target]]` to internal links `\ref{target-id}` or similar.
-- Cleans the target ID to match the slugification used in `builder.py`.
-- @param el The Link element.
function Link(el)
    if el.classes:includes("wikilink") then
        local target = el.target

        -- Check for anchor (e.g. "File#Heading")
        local file_part, anchor_part = target:match("^(.*)#(.*)$")

        local target_id = ""

        if anchor_part then
            -- If linking to a specific heading/anchor, slugify the anchor part
            anchor_part = anchor_part:match("^%s*(.-)%s*$")
            target_id = anchor_part:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
        else
            -- Clean the target to match build_book.py logic (remove leading numbers/punctuation)
            local clean_target = target:match("^[%d%s%.%-_]*(.*)") or target
            target_id = clean_target:lower():gsub("%s+", "-"):gsub("[^%w%-]", "")
        end

        local content = el.content

        -- If content is empty or matches the raw target (default behavior), use clean_target
        local content_text = pandoc.utils.stringify(content)
        if #content == 0 or content_text == target then
            -- Use the original target text (without the #part if we want, or just the whole thing)
            content = { pandoc.Str(target) }
        end

        return pandoc.Link(content, "#" .. target_id)
    end
end
