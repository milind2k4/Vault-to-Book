-- chemistry.lua
--[[
    Advanced Lua filter for handling chemical equations and math blocks.

    This filter processes `\ce{}` blocks to distinguish between complex chemical reactions
    and simple math/unit expressions. It cleans content, protects variables, and ensures
    compatibility with LaTeX split environments.
]]

-- Words that should be rendered as upright text (protected from chemical parsing)
local protected_words = {
    "Rate", "Heat", "fast", "slow", "Example", "Examples", "Graph", "vs", "surface"
}

-- Math variables that should be italicized ($var$) inside chemical contexts
local math_vars = {
    "k", "n", "x", "y"
}

--- Checks if a string contains Greek letters or math symbols.
-- @param s string The input string.
-- @return boolean True if math symbols are found.
local function has_math_symbols(s)
    return s:find("\\[a-zA-Z]+") or s:find("[_=^]")
end

--- Checks if a string contains complex reaction indicators (arrows).
-- Used to distinguish between chemical reactions (wrapped in \ce) and simple math (wrapped in \symup).
-- @param s string The input string.
-- @return boolean True if reaction arrows are found.
local function is_complex_reaction(s)
    -- Matches ->, <-, <=>, <->
    return s:find("%->") or s:find("<%-") or s:find("<=>")
end

--- Cleans and formats content intended for a \ce{...} block.
-- Applies rules for text protection, math variable sizing, and concentration term wrapping.
-- @param content string The raw content inside \ce{}.
-- @return string The cleaned content.
local function clean_chemistry_content(content)
    -- Optimization: Skip advanced processing for non-complex inputs
    if not is_complex_reaction(content) then
        return content
    end

    -- Strip internal newlines and collapse spaces
    content = content:gsub("[\n\r]", " ")
    content = content:gsub("%s+", " ")

    -- Text Protection: Wrap keywords in {Braces} to force upright text
    for _, word in ipairs(protected_words) do
        content = content:gsub("(%f[%w]" .. word .. "%f[%W])", "{%1}")
    end

    -- Arrow Argument Safety: Protect arguments in reaction arrows ->[arg]
    content = content:gsub("(%-%>%[)(.-)(%])", function(prefix, inner, suffix)
        if has_math_symbols(inner) then
            -- Wrap math content like \Delta in $...$ if not already present
            if not inner:find("%$") then
                return prefix .. "$" .. inner .. "$" .. suffix
            end
        else
            -- Wrap text arguments in {...}
            if not inner:find("{") then
                return prefix .. "{" .. inner .. "}" .. suffix
            end
        end
        return prefix .. inner .. suffix
    end)

    -- Concentration Protection: Wrap [A], [B] contents as [{A}]
    -- Handle start of string
    content = content:gsub("^(%s*)%[([%w]+)%]", "%1[{%2}]")
    -- Handle general case (not preceded by > to avoid arrow args)
    content = content:gsub("([^>])%[([%w]+)%]", "%1[{%2}]")

    -- Math Variable Handling: Wrap standalone vars in $...$ to ensure italicization
    for _, var in ipairs(math_vars) do
        -- Surrounded by spaces
        content = content:gsub("(%s+)" .. var .. "(%s+)", "%1$" .. var .. "$%2")
        -- At end of string
        content = content:gsub("(%s+)" .. var .. "$", "%1$" .. var .. "$")
        -- Standalone (frontier pattern)
        content = content:gsub("%f[%w]" .. var .. "%f[%W]", "$" .. var .. "$")
    end

    return content
end

--- Splits content by rows (\\) and columns (&) to apply a wrapper to each cell.
-- This ensures that LaTeX table delimiters like \\ and & remain outside the formatting command.
-- @param content string The raw content string.
-- @param wrapper string The LaTeX command to wrap each cell with (e.g. "\\ce", "\\symup").
-- @param is_complex boolean Whether to apply chemistry cleaning to the cell content.
-- @return string The processed content with wrappers applied to individual cells.
local function process_content_with_splitting(content, wrapper, is_complex)
    -- Helper to split string by delimiter
    local function split_by(str, delim)
        local res = {}
        local start = 1
        local delim_pattern = delim == "\\\\" and "\\\\" or delim

        while true do
            local s, e = str:find(delim_pattern, start)
            if not s then
                table.insert(res, str:sub(start))
                break
            end
            table.insert(res, str:sub(start, s - 1))
            start = e + 1
        end
        return res
    end

    local row_strs = split_by(content, "\\\\")
    local processed_rows = {}

    for _, r_str in ipairs(row_strs) do
        local col_strs = split_by(r_str, "&")
        local processed_cols = {}

        for _, c_str in ipairs(col_strs) do
            local final_cell = c_str
            if is_complex then
                final_cell = clean_chemistry_content(final_cell)
            end
            -- Wrap cell content
            table.insert(processed_cols, wrapper .. "{" .. final_cell .. "}")
        end

        table.insert(processed_rows, table.concat(processed_cols, "&"))
    end

    return table.concat(processed_rows, "\\\\")
end

--- Pandoc Filter Function for Math Elements.
-- Processes \ce{} blocks inside and outside of split environments.
-- @param el The Math element.
function Math(el)
    -- Check for split environment
    if el.text:find("\\begin{split}") then
        -- Process \ce blocks inside split
        local new_tex = el.text:gsub("\\ce(%b{})", function(ce_body)
            local content = ce_body:sub(2, -2)  -- Strip outer {}

            local complex = is_complex_reaction(content)
            local wrapper = complex and "\\ce" or "\\symup"

            return process_content_with_splitting(content, wrapper, complex)
        end)

        -- Clean up stray blank lines which break LaTeX math mode
        new_tex = new_tex:gsub("\n%s*\n", "\n")

        el.text = new_tex
        return el
    elseif el.text:find("\\ce") then
        -- Standard standalone \ce{...} processing
        local new_tex = el.text:gsub("\\ce(%b{})", function(ce_body)
            local content = ce_body:sub(2, -2)

            local complex = is_complex_reaction(content)
            local wrapper = complex and "\\ce" or "\\symup"

            return process_content_with_splitting(content, wrapper, complex)
        end)

        el.text = new_tex
        return el
    end
end
