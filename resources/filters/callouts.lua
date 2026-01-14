---@diagnostic disable: undefined-global
-- callouts.lua
-- Handles Obsidian Callouts (BlockQuotes).
-- Converts citation-style blockquotes `> [!INFO]` into LaTeX environments.

--- Handles Obsidian Callouts (BlockQuotes).
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
