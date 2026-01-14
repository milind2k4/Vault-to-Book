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

--- Fixes chemical equations by replacing `\ce{}` with `\symup{}` (or equivalent).
-- @param el The Math element.
function Math(el)
    -- Check for split environment first
    -- Check for split environment first
    if el.text:find("\\begin{split}") then
        -- Remove \ce{...} wrappers inside split, keeping content.
        -- We use %b{} to match balanced braces, e.g. {H2O} or {SO4^{2-}}.
        -- Then we strip the outer braces.
        local new_tex = el.text:gsub("\\ce(%b{})", function(body)
            return body:sub(2, -2) -- Return content without { and }
        end)

        -- FAILSAFE: Remove blank lines (double newlines) which act as \par and break 'split' environment
        -- Matches newline, optional whitespace, newline -> replaces with single newline
        new_tex = new_tex:gsub("\n%s*\n", "\n")

        el.text = new_tex
        return el
    elseif el.text:find("\\ce{") then
        local new_tex = el.text:gsub("\\ce", "\\symup")
        el.text = new_tex
        return el
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
