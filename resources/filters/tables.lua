---@diagnostic disable: undefined-global
-- tables.lua
-- Adjusts table column widths using a square-root scaling algorithm.

--- Adjusts table column widths using a square-root scaling algorithm.
-- Ensures that columns with more content get more space, but with diminishing returns.
-- Essential for preventing wide tables from overflowing the page.
-- @param el The Table element.
function Table(el)
    local colspecs = el.colspecs
    local needs_fix = false
    local count = #colspecs

    -- Smart Column Widths: Calculate based on content length
    -- 1. Scan header and body to find max char length per column
    local col_max_lens = {}
    for i = 1, count do col_max_lens[i] = 1 end -- Init with 1 to avoid div by zero

    -- Check Header
    local function get_cell_len(cell)
        -- Add a buffer (e.g., 4 chars) to help short words get more weight
        return #pandoc.utils.stringify(cell) + 4
    end

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

    -- Check Body (first 20 rows to save perf on huge tables)
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

    -- Assign Proportional Widths using Square Root Scaling
    -- This ensures short columns get relatively more space compared to linear scaling
    -- (e.g. sqrt(10)=3.1 vs sqrt(100)=10 is 1:3 ratio, whereas 10:100 is 1:10)

    local total_weight = 0
    local weights = {}

    for i = 1, count do
        local w = math.sqrt(col_max_lens[i])
        weights[i] = w
        total_weight = total_weight + w
    end

    for i, spec in ipairs(colspecs) do
        local w = weights[i]
        local percent = w / total_weight

        -- Enforce min width of 12% to avoid squashing
        if percent < 0.12 and count <= 6 then percent = 0.12 end

        spec[2] = percent * 0.98  -- Scale to 98% of page
    end

    -- Re-normalize
    local final_total = 0
    for _, spec in ipairs(colspecs) do final_total = final_total + spec[2] end
    if final_total > 0.99 then
        local scale = 0.98 / final_total
        for _, spec in ipairs(colspecs) do spec[2] = spec[2] * scale end
    end

    el.colspecs = colspecs
    return el
end
