Tasks:

- [ ] handle \ce blocks.

Prompt:
\ce is giving me a LOT of trouble. So i need you to make a separate lua file to handle \ce blocks.

I want it to handle everything effectively. Create a Lua module that processes a raw string intended for a \ce{...} block and applies the following cleaning rules:

1. Text Protection (The "Rate" vs "RaTe" fix):

    Identify words that are clearly non-chemical text (e.g., "Rate", "Heat", "fast", "slow") inside the block.

    Automatically wrap these words in curly braces {...} so mhchem renders them as upright text instead of trying to parse them as chemical elements.

2. Math Variable Handling:

    Identify standalone variables often used in rate laws or stoichiometry (like k, n, x, y) that are NOT chemical symbols.

    Wrap these in $...$ so they render as italicized math variables.

3. Arrow Argument Safety:

    If the string contains reaction arrows with conditions (e.g., ->[hv]), ensure the content inside the brackets is handled correctly. If it contains Greek letters or physics constants (like hv), wrap the inside in $ (e.g., ->[$h\nu$]).

4. Whitespace Cleanup:

    Strip any internal newlines or double-returns within the string to prevent LaTeX compilation errors (since \ce and math blocks fail on blank lines).

5. Syntax Preservation:

    Ensure standard chemical syntax (like H2O, +, ->) remains untouched.

6. Alignment Tab Handling (The & Fix):

    Check if the \ce{...} string contains the ampersand & symbol (used for alignment in split/align environments).

    You cannot leave & inside the \ce tag because the LaTeX compiler needs to see it to align the columns.

    Action: Split the \ce block into separate parts around the &.

    Example Input: \ce{Zn & -> Zn^{+2} + 2e^-}

    Example Output: \ce{ Zn } & \ce{ -> Zn^{+2} + 2e^- }

Keep the current handling where if a \ce block is inside the split environment, remove it. So basically, i need the 6th one to handle cases where there are chemical reactions inside \ce inside the split environment.