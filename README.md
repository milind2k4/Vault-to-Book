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

### 1. Import Vault
Prepare your notes by importing them from your Obsidian vault.
```bash
python import_vault.py --source "E:\Obsidian\MyVault" --output "MyBook"
```

### 2. Build PDF
Convert the imported notes into a PDF.
```bash
python build_book.py
```

## Configuration
Edit `config.yaml` to change:
- Book Title/Author
- Fonts and Colors
- Margins
- Mermaid settings
