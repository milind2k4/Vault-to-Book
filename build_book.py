import os
import re
import subprocess
import sys

# --- Configuration ---
SOURCE_DIR = "Java" # Change this to your vault directory
OUTPUT_FILE = "java.pdf"
TEMPLATE_FILE = "eisvogel.latex"
PDF_ENGINE = "xelatex" # pdflatex or xelatex (recommended for custom fonts)
MAINFONT = "LMRoman10-Regular" # "Charis SIL" or None
SANSFONT = "Arial" # "Lato" or None
MONOFONT = "LMMono10-Regular" # "Fira Code" or None
# ---------------------

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    return text

def clean_title(filename):
    base = os.path.splitext(filename)[0]
    match = re.match(r'^[\d\s\.\-_]+(.*)', base)
    if match:
        title = match.group(1).strip()
        if title: return title
    return base.strip()

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    title = clean_title(filename)
    file_id = slugify(title)

    lines = content.split('\n')
    new_lines = []
    
    first_header_removed = False
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Remove "Links:" line and following underscores
        if stripped.lower().startswith("links:"):
            continue
        # 2. Remove lines that are just underscores (like horizontal rules)
        if re.match(r'^_+$', stripped):
            continue
        
        # 3. Remove the FIRST header if it matches the title (or just any first header)
        if stripped.startswith('#') and not first_header_removed:
            if re.match(r'^#+\s', line):
                first_header_removed = True
                continue

        # Demote remaining headers
        if stripped.startswith('#'):
             if re.match(r'^#+\s', line):
                 line = '#' + line
                 
        new_lines.append(line)
        
    content = '\n'.join(new_lines)
    # content = re.sub(r'(?m)^\s*_{3,}\s*$', '---', content)
    
    return title, content, file_id

def main():
    source_dir = os.path.abspath(SOURCE_DIR)
    temp_file = os.path.join(source_dir, "temp_master.md")
    
    print(f"Scanning {source_dir}...")
    
    md_files = []
    for root, dirs, files in os.walk(source_dir):
        if '.obsidian' in dirs: dirs.remove('.obsidian')
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            if file.lower().endswith(".md") and file != "temp_master.md":
                md_files.append(os.path.join(root, file))

    md_files.sort(key=lambda p: os.path.basename(p).lower())

    if not md_files:
        print("No markdown files found!")
        return

    print(f"Found {len(md_files)} files.")

    master_content = []
    
    # Add YAML metadata for setup (Using strikeout for highlights)
    # No extra yaml needed as we pass variables via CLI

    for filepath in md_files:
        title, content, fid = process_file(filepath)
        header = f"\n\n# {title} {{#{fid}}}\n\n"
        master_content.append(header)
        master_content.append(content)
        master_content.append("\n\n\\newpage\n\n")

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("".join(master_content))

    print(f"Created {temp_file}")
    
    # Template resolution
    template_arg = "eisvogel"
    possible_paths = [
        os.path.join(source_dir, TEMPLATE_FILE),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), TEMPLATE_FILE),
        TEMPLATE_FILE
    ]
    for p in possible_paths:
        if os.path.exists(p):
            template_arg = os.path.abspath(p)
            break
            
    # Filter resolution
    filter_arg = "obsidian_filter.lua"
    possible_filters = [
        os.path.join(source_dir, "obsidian_filter.lua"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "obsidian_filter.lua"),
        "obsidian_filter.lua"
    ]
    for p in possible_filters:
        if os.path.exists(p):
            filter_arg = os.path.abspath(p)
            break

    # 1. Generate LaTeX (Pandoc)
    tex_file = OUTPUT_FILE.replace(".pdf", ".tex")
    
    cmd_tex = [
        "pandoc",
        temp_file,
        "-o", tex_file,
        "--from", "markdown+wikilinks_title_after_pipe+mark+task_lists+tex_math_dollars",
        "--template", template_arg,
        "--lua-filter", filter_arg,
        "--syntax-highlighting=tango",
        "--table-of-contents",
        "--toc-depth=3",
        "--number-sections",
        "--top-level-division=chapter",
        "--variable", "book=true",
        "--variable", "strikeout=true",
        "--standalone"
    ]
    
    if MAINFONT: cmd_tex.extend(["--variable", f"mainfont={MAINFONT}"])
    if SANSFONT: cmd_tex.extend(["--variable", f"sansfont={SANSFONT}"])
    if MONOFONT: cmd_tex.extend(["--variable", f"monofont={MONOFONT}"])
    
    print(f"Generating LaTeX: {tex_file}...")
    try:
        subprocess.run(cmd_tex, check=True, cwd=source_dir)
        print(f"Done! {tex_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating LaTeX: {e}")
        return

    # 2. Compile LaTeX to PDF (xelatex)
    print(f"Compiling PDF from {tex_file} using {PDF_ENGINE}...")
    
    # Run twice for TOC resolution
    tex_cmd = [PDF_ENGINE, "-interaction=nonstopmode", tex_file]
    
    try:
        print("Pass 1/2...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir)
        print("Pass 2/2...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir)
        print(f"Done! Created {OUTPUT_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling PDF: {e}")
        print("Check the .log file for details.")

if __name__ == "__main__":
    main()
