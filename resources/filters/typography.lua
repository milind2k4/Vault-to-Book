---@diagnostic disable: undefined-global
-- typography.lua
-- Handles special characters, chemical equations, and highlighting.

--- Handles special characters like checkboxes.
-- @param el The Str element.
function Str(el)
    if el.text == "☐" then
        return pandoc.RawInline("latex", "$\\square$")
    elseif el.text == "☒" then
        return pandoc.RawInline("latex", "$\\boxtimes$")
    end
end

-- Math function removed (moved to chemistry.lua)

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
