# Vault-to-Book

A robust tool to convert Obsidian vaults into professional PDF books using Python, Pandoc, and XeLaTeX.

## Features
- **Obsidian Compatibility**: Handles wiki-links, attachments, and folder structures.
- **Mermaid Support**: Automatically converts Mermaid diagrams to high-res images.
- **Professional Layout**: Uses the Eisvogel LaTeX template.
- **Automated Build**: Handles multiple LaTeX passes for TOC generation.

## Prerequisites
- **Python 3.8+**
- **Pandoc** (Install via `choco install pandoc` or download from pandoc.org)
- **MiKTeX** or **TeX Live** (for `xelatex`)
- **Node.js** (for Mermaid CLI)
- **Mermaid CLI**: Install via `npm install -g @mermaid-js/mermaid-cli`

## Setup
1.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure `resources/` folder contains:
    - `eisvogel.latex`
    - `obsidian_filter.lua`
    - `callouts.tex`

## Usage

Run the `main.py` script to import your vault and build the PDF in a single step.

```bash
python main.py "path/to/notes" "path/to/attachments" [OPTIONS]
```

### Examples

**Basic Usage:**
```bash
python main.py "E:\Obsidian\MyVault" "E:\Obsidian\Attachments"
```

**Custom Title & Author:**
```bash
python main.py "E:\Obsidian\DBMS" "E:\Obsidian\Images" --title "Database Systems" --author "Jane Doe"
```

**Clean Release Build (Strict):**
Generates the PDF, moves it to the output path, and deletes all intermediate build files.
```bash
python main.py "E:\Obsidian\Java" "E:\Obsidian\Images" --cleanup strict --output-pdf "JavaBook.pdf"
```

**Using a Specific Build Directory:**
Perform the build in a specific folder (e.g., `tmp_build`) to keep your root clean.
```bash
python main.py "source" "attachments" --build-path "tmp_build"
```

### Arguments

| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `notes_dir` | (Positional) | Path to the source Obsidian vault folder | Required |
| `attachments_dir` | (Positional) | Path to the global Attachments folder | Required |
| `--title` | `-t` | Book title | Folder Name |
| `--subtitle` | `-s` | Book subtitle | "Personal Notes..." |
| `--author` | `-a` | Book author | "Anonymous" |
| `--cleanup` | `-c` | Cleanup strategy (`none`, `latex`, `artifacts`, `strict`) | `latex` |
| `--output-pdf` | `-o` | Specific output path for the PDF | None |
| `--build-path` | `-bp` | Directory where build takes place | Same as Title |

## Configuration
Edit `config.yaml` to change global style settings:
- Fonts and Colors
- Margins and Geometry
- Mermaid settings

*Note: Book metadata (Title/Author) is set via CLI args.*
