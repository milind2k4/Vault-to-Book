-- tables.lua
--[[
    Lua filter for intelligent table column sizing.

    Implements a specific algorithm (Square Root Scaling) to calculate relative
    column widths based on content length. This prevents wide tables from overflow
    and ensures better space distribution than linear scaling or equal widths.
]]

---@diagnostic disable: undefined-global

--- Adjusts table column widths using a square-root scaling algorithm.
-- Scans table headers and a subset of the body rows to determine optimal widths.
-- @param el The Table element.
function Table(el)
    local colspecs = el.colspecs
    local count = #colspecs
    local col_max_lens = {}

    -- Initialize max lengths
    for i = 1, count do col_max_lens[i] = 1 end

    --- Calculates formatted length of a cell with a buffer.
    local function get_cell_len(cell)
        return #pandoc.utils.stringify(cell) + 4
    end

    -- 1. Scan Header
    if el.head then
        for _, row in ipairs(el.head.rows) do
            for i, cell in ipairs(row.cells) do
                if i <= count then
                    local len = get_cell_len(cell)
                    if len > col_max_lens[i] then col_max_lens[i] = len end
                end
            end
        end
    end

    -- 2. Scan Body (Limit to first 20 rows for performance)
    for _, body in ipairs(el.bodies) do
        for r_idx, row in ipairs(body.body) do
            if r_idx > 20 then break end
            for i, cell in ipairs(row.cells) do
                if i <= count then
                    local len = get_cell_len(cell)
                    if len > col_max_lens[i] then col_max_lens[i] = len end
                end
            end
        end
    end

    -- 3. Assign Weights (Square Root Scaling)
    -- sqrt(len) provides diminishing returns for very long content,
    -- ensuring short columns don't get squashed.
    local total_weight = 0
    local weights = {}

    for i = 1, count do
        local w = math.sqrt(col_max_lens[i])
        weights[i] = w
        total_weight = total_weight + w
    end

    -- 4. Apply Widths
    for i, spec in ipairs(colspecs) do
        local w = weights[i]
        local percent = w / total_weight

        -- Enforce minimum width (12%) for small tables to avoid squashing
        if percent < 0.12 and count <= 6 then percent = 0.12 end

        -- Target 98% of text width
        spec[2] = percent * 0.98
    end

    -- 5. Re-normalize to ensure strict fit
    local final_total = 0
    for _, spec in ipairs(colspecs) do final_total = final_total + spec[2] end
    if final_total > 0.99 then
        local scale = 0.98 / final_total
        for _, spec in ipairs(colspecs) do spec[2] = spec[2] * scale end
    end

    el.colspecs = colspecs
    return el
end
