-- chemistry.lua
-- Advanced handling for \ce{...} blocks

-- List of words that should be protected as text {Word} inside \ce
local protected_words = {
    "Rate", "Heat", "fast", "slow", "Example", "Examples", "Graph", "vs", "surface"
}

-- List of math variables that should be italicized $var$
local math_vars = {
    "k", "n", "x", "y"
}

-- Helper to check if a string contains any Greek letters or math symbols
local function has_math_symbols(s)
    return s:find("\\[a-zA-Z]+") or s:find("[_=^]")
end

-- Helper to check if a string contains reaction indicators (arrows)
local function is_complex_reaction(s)
    -- Matches ->, <-, <=>, <->
    -- We specifically look for arrows. Plain "=" is math, not necessarily chemistry.
    return s:find("%->") or s:find("<%-") or s:find("<=>")
end

local function clean_chemistry_content(content)
    -- OPTIMIZATION: If not a complex reaction, user requests to skip advanced processing.
    -- "Rate" equations contain "=" or "->".
    -- Simple species like H2O don't.
    if not is_complex_reaction(content) then
        return content
    end

    -- 4. Whitespace Cleanup: Strip internal newlines
    content = content:gsub("[\n\r]", " ")
    content = content:gsub("%s+", " ") -- Collapse multiple spaces

    -- 1. Text Protection (Rate, Heat, etc.)
    for _, word in ipairs(protected_words) do
        -- Patterns:
        -- Avoid matching inside other words (e.g. heated).
        -- Match word boundaries or distinct usage.
        -- We'll use %f[%w] frontier pattern for word boundaries.

        -- If it's already in braces {Rate}, skip.
        -- If it's "Rate = k", we want "{Rate} = $k$"

        -- Wrap word in {} if not already wrapped
        -- Using simple replacement for known keywords
        -- Note: Lua patterns are limited. We'll do a simple scan.
        content = content:gsub("(%f[%w]" .. word .. "%f[%W])", "{%1}")
    end

    -- User Request: "Rate = k" -> "{Rate} = $k$"
    -- Also handle phrases like "gold surface" -> "{gold surface}"
    -- The user example: "gold surface". "gold" isn't in my list, but "surface" is.
    -- If we see "word surface", maybe protect both?
    -- For now, let's explicitly add "gold" to protected words if needed, or rely on specific patterns.
    -- User comment example: "gold surface". Let's handle generic text detection if possible?
    -- Hard to distinguish "Ni" (Nickel) from "If" (text).
    -- We will stick to the provided list and the "gold surface" specific case if it comes up often,
    -- OR just wrap specific known text phrases.
    -- Let's add "gold" to the loop dynamically? No, that's risky logic.
    -- I'll stick to the specific word replacement for now.
    -- Actually, simpler: The user wants "gold surface" -> "{gold surface}".
    -- Maybe detecting [ ... text ... ] brackets for arrows?

    -- 3. Arrow Argument Safety
    -- Match ->[arg1] or ->[arg1][arg2]
    -- We can capture the content inside []
    content = content:gsub("(%-%>%[)(.-)(%])", function(prefix, inner, suffix)
        if has_math_symbols(inner) then
            -- Wrap in $...$ e.g. \Delta -> $\Delta$
            -- Check if already wrapped?
            if not inner:find("%$") then
                return prefix .. "$" .. inner .. "$" .. suffix
            end
        else
            -- Likely text, wrap in {...} e.g. gold surface
            -- But check if it looks like a chemical formula?
            -- Safest to assume arguments are text/conditions unless they look like math.
            -- "gold surface" has space, chemical formulas usually don't have space inside []
            if not inner:find("{") then
                return prefix .. "{" .. inner .. "}" .. suffix
            end
        end
        return prefix .. inner .. suffix
    end)

    -- 7. Concentration Protection (User Request: [A], [B])
    -- Wrap content of [A], [B] in {} -> [{A}].
    -- Ensure we don't wrap arrow arguments like ->[fast].
    -- We check that the preceding char is not '>'.

    -- Handle start of string:
    content = content:gsub("^(%s*)%[([%w]+)%]", "%1[{%2}]")

    -- Handle general case (not preceded by >):
    -- Pattern: Capture 1 (non-> char), match [, Capture 2 (content), match ]
    content = content:gsub("([^>])%[([%w]+)%]", "%1[{%2}]")

    -- 2. Math Variable Handling independent of arrow
    -- "Rate = k". We already protected {Rate}. Now " = k".
    -- "k" is a stand alone char here.
    for _, var in ipairs(math_vars) do
        -- Match var surrounded by spaces
        -- Capture 1: space prefix, Capture 2: space suffix
        content = content:gsub("(%s+)" .. var .. "(%s+)", "%1$" .. var .. "$%2")

        -- Match var at end of string with space prefix
        -- Capture 1: space prefix
        content = content:gsub("(%s+)" .. var .. "$", "%1$" .. var .. "$")

        -- Match " = k" or similar (start of string or after non-word?)
        -- Simplest: Usage of frontier pattern like earlier
        -- %f[%w]var%f[%W] matches standalone var
        content = content:gsub("%f[%w]" .. var .. "%f[%W]", "$" .. var .. "$")
    end

    -- Specific Fix: "Rate = k" -> "Rate" is {Rate}, "k" is $k$.
    -- ensure comma separation handling? "H2 + I2, Rate = k"
    -- mhchem naturally handles commas (usually).

    return content
end

-- Helper to process content by splitting rows (\\) and columns (&)
-- Ensures that \\ and & remain outside the wrapper (e.g. \symup{...} & \symup{...} \\)
local function process_content_with_splitting(content, wrapper, is_complex)
    local rows = {}
    -- Split by double backslash \\
    -- Pattern: non-greedy match until \\ or end
    -- Iterating carefully. Lua gmatch "[^\\\\]+" is risky for escaped chars.
    -- We can use a simple split approach by replacing delimiter.

    -- Placeholder for split logic:
    local n = 1
    for row in (content .. "\\\\"):gmatch("(.-)\\\\") do
        if row ~= "" or n < #content then -- Avoid empty last capture if spurious
            -- Process Columns in this row
            local cols = {}
            for col in (row .. "&"):gmatch("(.-)&") do
                -- Check if we hit the end of the string loop (hacky splitter)
                -- Better: gmatch all segments.
            end
        end
        n = n + 1
    end

    -- Cleaner approach: Custom split function
    local function split_by(str, delim)
        local res = {}
        local start = 1
        -- special case for \\ which is regex special
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
        -- Skip empty rows if they are just trailing artifacts?
        -- No, empty rows might be intentional vertical space.
        -- But split_by returns empty string for "A\\" -> "A", "".

        -- Inner split by &
        local col_strs = split_by(r_str, "&")
        local processed_cols = {}

        for _, c_str in ipairs(col_strs) do
            -- Trim whitespace?
            -- Only trim strictly necessary? LateX handles space.
            -- But we want to detect empty cells maybe?

            -- Apply chemistry cleaning if complex
            local final_cell = c_str
            if is_complex then
                final_cell = clean_chemistry_content(final_cell)
            end

            -- Wrap
            -- Don't wrap empty content? \symup{} is fine.
            table.insert(processed_cols, wrapper .. "{" .. final_cell .. "}")
        end

        table.insert(processed_rows, table.concat(processed_cols, "&"))
    end

    -- Rejoin with \\
    -- If the original had trailing \\, split_by produces a trailing empty part.
    -- We rejoin all parts.
    -- Note: If original was "A \\ B", split -> "A", " B". Join -> "A \\ B".
    -- If original "A \\", split -> "A", "". Join -> "A \\ ". Correct.
    return table.concat(processed_rows, "\\\\")
end

function Math(el)
    -- Start by handling \ce{} blocks
    -- Check for split environment first (superseding typography.lua)
    if el.text:find("\\begin{split}") then
        -- Rule: Inside split, we must apply Rule 6 (Split by &).

        -- 1. Identify \ce blocks
        -- Use %b{} to find balanced braces \ce{...}
        local new_tex = el.text:gsub("\\ce(%b{})", function(ce_body)
            local content = ce_body:sub(2, -2)  -- Strip outer {}

            -- Check complexity
            local complex = is_complex_reaction(content)
            local wrapper = complex and "\\ce" or "\\symup"

            return process_content_with_splitting(content, wrapper, complex)
        end)

        -- Failsafe: Remove blank lines inside the split environment (global cleanup)
        new_tex = new_tex:gsub("\n%s*\n", "\n")

        el.text = new_tex
        return el
    elseif el.text:find("\\ce") then
        -- Standard standalone \ce{...}
        local new_tex = el.text:gsub("\\ce(%b{})", function(ce_body)
            local content = ce_body:sub(2, -2)

            -- Check complexity
            local complex = is_complex_reaction(content)
            local wrapper = complex and "\\ce" or "\\symup"

            return process_content_with_splitting(content, wrapper, complex)
        end)

        el.text = new_tex
        return el
    end
end
