-- typography.lua
--[[
    Lua filter for miscellaneous typography adjustments.

    Handles:
    - Substitution of special characters (checkboxes).
    - Highlighting syntax `==text==` -> `\hl{text}`.
]]

---@diagnostic disable: undefined-global

--- Replaces specific Unicode characters with LaTeX symbols.
-- Handles checkboxes: `☐` -> `\square`, `☒` -> `\boxtimes`.
-- @param el The Str element.
function Str(el)
    if el.text == "☐" then
        return pandoc.RawInline("latex", "$\\square$")
    elseif el.text == "☒" then
        return pandoc.RawInline("latex", "$\\boxtimes$")
    end
end

--- Converts highlighted text (Pandoc Mark) to LaTeX highlight command.
-- Transforms `==text==` syntax (Mark) into `\hl{text}`.
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
