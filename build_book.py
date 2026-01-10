import os
import re
import subprocess
import sys

# --- Configuration ---
SOURCE_DIR = os.getenv("SOURCE_DIR", "Java") # Change this to your vault directory
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "java.pdf")
TEMPLATE_FILE = "eisvogel.latex"
PDF_ENGINE = "xelatex" # pdflatex or xelatex (recommended for custom fonts)
MAINFONT = "LMRoman10-Regular" # "Charis SIL" or None
SANSFONT = "Arial" # "Lato" or None
MONOFONT = "LMMono10-Regular" # "Fira Code" or None
# Link Colors (Hex codes without #)
LINKCOLOR = "07455c"  # Standard Blue
URLCOLOR = LINKCOLOR   # Standard Blue
MERMAID_DEFAULT_WIDTH = None # Width in cm (or %)
MERMAID_DEFAULT_HEIGHT = "11cm"  # Height in cm (e.g. "8cm"). If set, overrides width.
CHAPTER_TOP_MARGIN = "0pt" # Distance from top of page to Chapter Title (negative moves up)
CHAPTER_BOTTOM_MARGIN = "20pt" # Distance from bottom of page to Chapter Title (negative moves up)
BOOK_TITLE = os.getenv("BOOK_TITLE", "Java")
BOOK_SUBTITLE = os.getenv("BOOK_SUBTITLE", "Personal Notes & References")
BOOK_AUTHOR = os.getenv("BOOK_AUTHOR", "Milind")
# ---------------------

def clean_title(filename):
    """
    Extracts a clean title from the filename.
    Removes leading numbers (01, 01_, 01 -, etc.) and extension.
    """
    base = os.path.splitext(filename)[0]
    # Remove leading numbering patterns like "01 ", "01_", "01-", "1. "
    cleaned = re.sub(r'^[\d\s\.\-_]+', '', base)
    return cleaned.strip()

def slugify(text):
    """
    Creates a simple ID from text.
    """
    return re.sub(r'[^a-zA-Z0-9-]', '', text.lower().replace(' ', '-'))

import hashlib

def process_mermaid(content, source_dir):
    """
    Finds mermaid blocks, generates images using mmdc, and replaces blocks with image links.
    """
    # Regex to find mermaid blocks: ```mermaid ... ```
    pattern = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
    
    images_dir = os.path.join(source_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    def replacer(match):
        mermaid_code = match.group(1).strip()
        
        # Parse configuration from comments
        # Syntax: %% width=14cm %% or %% height=5cm %% or %% scale=4 %%
        width = MERMAID_DEFAULT_WIDTH
        height = MERMAID_DEFAULT_HEIGHT
        scale = 3.0 # Default High Quality
        
        width_match = re.search(r'%%\s*width=([^\s%]+%?)\s*%%', mermaid_code, re.IGNORECASE)
        if width_match:
            width = width_match.group(1)

        height_match = re.search(r'%%\s*height=([^\s%]+%?)\s*%%', mermaid_code, re.IGNORECASE)
        if height_match:
            height = height_match.group(1)
            
        scale_match = re.search(r'%%\s*scale=([\d\.]+)\s*%%', mermaid_code, re.IGNORECASE)
        if scale_match:
            try:
                scale = float(scale_match.group(1))
            except ValueError:
                pass

        # Create hash of the code + config to ensure regeneration on change
        config_str = f"{mermaid_code}|{scale}|{width}|{height}"
        code_hash = hashlib.md5(config_str.encode('utf-8')).hexdigest()
        image_filename = f"mermaid_{code_hash}.png"
        image_path = os.path.join(images_dir, image_filename)
        
        # Only generate if it doesn't exist
        if not os.path.exists(image_path):
            mmd_file = os.path.join(images_dir, f"temp_{code_hash}.mmd")
            with open(mmd_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            
            # Use cmd /c to ensure it runs even if PS scripts are disabled
            # -s for scale
            cmd = f'cmd /c mmdc -i "{mmd_file}" -o "{image_path}" -b transparent -s {scale}'
            try:
                print(f"Generating Mermaid diagram: {image_filename} (scale={scale})...")
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"Failed to generate mermaid diagram {image_filename}")
                return match.group(0) # Return original on failure
            finally:
                if os.path.exists(mmd_file):
                    os.remove(mmd_file)
        
        # Return markdown image link with prioritization
        # Use escaped space caption "![\\ ]" to force Figure environment
        # Combined with \captionsetup{labelsep=none}, this produces "Figure 1.1" centered.
        if height:
             # Height takes priority, width is ignored
            return f"![\\ ](images/{image_filename}){{height={height}}}"
        elif width:
            return f"![\\ ](images/{image_filename}){{width={width}}}"
        else:
            return f"![\\ ](images/{image_filename})" # Default size

    return pattern.sub(replacer, content)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process Mermaid BEFORE other cleanup
    source_dir = os.path.dirname(filepath)
    # We need to pass the root source dir or handle images relative to where python runs.
    # Let's assume images go into SOURCE_DIR/images for simplicity
    valid_source_dir = os.path.abspath(SOURCE_DIR)
    content = process_mermaid(content, valid_source_dir)

    filename = os.path.basename(filepath)
    title = clean_title(filename)
    file_id = slugify(title)

    lines = content.split('\n')
    new_lines = []
    
    first_header_removed = False
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Remove "Links:" line
        if re.match(r'^links:?', stripped, re.IGNORECASE):
            continue
            
        # 2. Remove horizontal rules (underscores, dashes, asterisks)
        if re.match(r'^\s*[-_*]{3,}\s*$', stripped):
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
    
    # 1. Create headers.tex with dynamic setup
    # Note: We use absolute path for logo in the tex file
    logo_tex_path = os.path.join(source_dir, "images", "logo.png").replace("\\", "/")
    
    headers_tex_content = f"""
\\usepackage{{caption}}
\\captionsetup[figure]{{labelsep=none, justification=centering}}
\\usepackage{{minitoc}}
\\mtcselectlanguage{{english}}
\\definecolor{{mylinkcolor}}{{HTML}}{{{LINKCOLOR}}}
\\definecolor{{myurlcolor}}{{HTML}}{{{URLCOLOR}}}
% --- Chapter Title Styling (KOMA-Script) ---
\\renewcommand*\\chapterformat{{\\thechapter.\\enskip}}
\\addtokomafont{{chapter}}{{\\centering}}
\\RedeclareSectionCommand[beforeskip={CHAPTER_TOP_MARGIN},afterskip={CHAPTER_BOTTOM_MARGIN}]{{chapter}}
% --- Table Styling ---
\\rowcolors{{2}}{{RoyalBlue!20}}{{white}}
\\renewcommand{{\\arraystretch}}{{1.2}}
% -------------------------------------------
"""
    headers_tex_file = os.path.join(source_dir, "headers.tex")
    with open(headers_tex_file, 'w', encoding='utf-8') as f:
        f.write(headers_tex_content)

    # 2. Setup Date and Cover Page
    from datetime import date
    current_date = date.today().strftime("%B %d, %Y")

    cover_tex_path = os.path.join(source_dir, "cover.tex")
    
    # Conditional Logo
    logo_block = ""
    if os.path.exists(os.path.join(source_dir, "images", "logo.png")):
        logo_block = f"""
    \\begin{{flushright}}
        \\includegraphics[width=4cm]{{{logo_tex_path}}}
    \\end{{flushright}}
    """

    cover_content = f"""
\\begin{{titlepage}}
    \\newgeometry{{left=2.5cm,right=2.5cm,top=2cm,bottom=2cm}}
    \\vspace*{{1cm}}
    {logo_block}
    
    \\vspace{{3cm}}
    
    \\centering
    {{\\fontsize{{50}}{{60}}\\selectfont \\bfseries {BOOK_TITLE} \\par}}
    \\vspace{{1cm}}
    {{\\fontsize{{20}}{{30}}\\selectfont {BOOK_SUBTITLE.replace("&", "\\&")} \\par}}
    
    \\vfill
    
    {{\\fontsize{{18}}{{22}}\\selectfont {BOOK_AUTHOR} \\par}}
    \\vspace{{0.5cm}}
    {{\\large {current_date} \\par}}
    
    \\vspace{{3cm}}
    \\restoregeometry
\\end{{titlepage}}
"""
    with open(cover_tex_path, 'w', encoding='utf-8') as f:
        f.write(cover_content)

    # Simplified YAML block
    yaml_block = f"""---
include-before:
  - \\dominitoc
  - \\setcounter{{minitocdepth}}{{4}}
---

"""
    master_content.append(yaml_block)

    for filepath in md_files:
        title, content, fid = process_file(filepath)
        # Add Chapter Header + Mini TOC
        # \\minitoc must be protected or raw latex
        header = f"\n\n# {title} {{#{fid}}}\n\n\\minitoc\n\n"
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
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    callouts_src = os.path.join(script_dir, "callouts.tex")
    
    cmd_tex = [
        "pandoc",
        temp_file,
        "-o", tex_file,
        "--from", "markdown+wikilinks_title_after_pipe+mark+task_lists+tex_math_dollars",
        "--template", template_arg,
        "--include-before-body", cover_tex_path,
        "--metadata", f"title={BOOK_TITLE}",
        "--metadata", f"subtitle={BOOK_SUBTITLE}",
        "--metadata", f"author={BOOK_AUTHOR}",
        "--metadata", f"date={current_date}",
        "--include-in-header", headers_tex_file,
        "--include-in-header", callouts_src,
        "--lua-filter", filter_arg,
        "--syntax-highlighting=tango",
        "--table-of-contents",
        "--toc-depth=4",
        "--number-sections",
        "--top-level-division=chapter",
        "--variable", "book=true",
        "--variable", "strikeout=true",
        "--variable", "classoption=openany", # Removes blank pages
        "--variable", "classoption=oneside", # Optional: better for digital reading
        "--variable", "colorlinks=true", # Make links visible
        "--variable", "linkcolor=mylinkcolor",
        "--variable", "urlcolor=myurlcolor",
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
    
    # Run 3 times for TOC/MiniTOC resolution
    tex_cmd = [PDF_ENGINE, "-interaction=nonstopmode", tex_file]
    
    try:
        print("Pass 1/3 (Init)...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir)
        print("Pass 2/3 (TOC)...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir)
        print("Pass 3/3 (Refs/MiniTOC)...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir)
        print(f"Done! Created {OUTPUT_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling PDF: {e}")
        print("Check the .log file for details.")

if __name__ == "__main__":
    main()
