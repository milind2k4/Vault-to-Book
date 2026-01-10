import os
import re
import subprocess
import shutil
import sys
from .config import CONFIG
from .utils import clean_title, slugify, ensure_dir
from .mermaider import process_mermaid
from .tex_manager import generate_headers_tex, generate_cover_tex
from .cleaner import cleanup_artifacts

def process_file(filepath: str, source_dir: str) -> tuple[str, str, str]:
    """
    Reads a markdown file, processes it (mermaid, etc), and returns title/content/id.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process Mermaid
    content = process_mermaid(content, source_dir)

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
            
        # 2. Remove horizontal rules
        if re.match(r'^\s*[-_*]{3,}\s*$', stripped):
            continue
        
        # 3. Remove the FIRST header if it matches the title (or just any first header)
        if stripped.startswith('#') and not first_header_removed:
            if re.match(r'^#+\s', line):
                first_header_removed = True
                continue
 
        new_lines.append(line)
        
    content = '\n'.join(new_lines)
    
    return title, content, file_id

def build() -> None:
    source_dir = os.path.abspath(CONFIG['build']['source_dir'])
    output_file = CONFIG['build']['output_file']
    pdf_engine = CONFIG['build']['pdf_engine']
    artifacts_dir_name = CONFIG['build'].get('artifacts_dir', 'build_artifacts')
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        print("Please set 'source_dir' in config.yaml or run import_vault.py first.")
        return

    # Create artifacts directory
    artifacts_dir = os.path.join(source_dir, artifacts_dir_name)
    ensure_dir(artifacts_dir)
    print(f"Build artifacts will be stored in: {artifacts_dir}")

    temp_file = os.path.join(artifacts_dir, "temp_master.md")
    
    print(f"Scanning {source_dir}...")
    
    md_files = []
    for root, dirs, files in os.walk(source_dir):
        if '.obsidian' in dirs: dirs.remove('.obsidian')
        if '.git' in dirs: dirs.remove('.git')
        # Skip the artifacts directory itself to avoid recursion if it's inside source_dir
        if artifacts_dir_name in dirs: dirs.remove(artifacts_dir_name)
        
        for file in files:
            if file.lower().endswith(".md") and file != "temp_master.md":
                md_files.append(os.path.join(root, file))

    md_files.sort(key=lambda p: os.path.basename(p).lower())

    if not md_files:
        print("No markdown files found!")
        return

    print(f"Found {len(md_files)} files.\n")

    master_content = []
    
    # 1. Generate Headers and Cover (put them in artifacts_dir)
    headers_tex_file = generate_headers_tex(artifacts_dir)
    cover_tex_path = generate_cover_tex(artifacts_dir) # Only content changes? No, it writes file.

    # YAML block removed, minitoc init moved to cover.tex

    for filepath in md_files:
        title, content, fid = process_file(filepath, source_dir)
        # Add Chapter Header + Mini TOC (using etoc)
        # We style it to look like a mini TOC box
        header = f"""

# {title} {{#{fid}}}

\\etocsettocstyle{{\\textbf{{Chapter Contents}}\\par\\rule{{\\linewidth}}{{0.5pt}}}}{{\\par\\rule{{\\linewidth}}{{0.5pt}}}}
\\localtableofcontents
\\noindent

"""
        master_content.append(header)
        master_content.append(content)
        master_content.append("\n\n\\newpage\n\n")

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("".join(master_content))

    print(f"Created {temp_file}")
    
    # Resource Resolution
    resource_dir = CONFIG['resources']['dir']
    template_name = CONFIG['style']['template']
    
    def resolve_resource(name: str) -> str:
        paths = [
            os.path.join(resource_dir, name),
            name
        ]
        for p in paths:
            if os.path.exists(p):
                return os.path.abspath(p)
        return name

    template_arg = resolve_resource(template_name)
    filter_arg = resolve_resource("obsidian_filter.lua")
    callouts_arg = resolve_resource("callouts.tex")

    # 1. Generate LaTeX (Pandoc)
    # Output tex file in artifacts_dir
    tex_file_name = output_file.replace(".pdf", ".tex")
    tex_file = os.path.join(artifacts_dir, tex_file_name)
    
    # Prepare Cover Path for Pandoc (needs to be absolute or relative to CWD)
    # We will run pandoc from source_dir so that images (which are links like "images/foo.png") work.
    
    cmd_tex = [
        "pandoc",
        os.path.relpath(temp_file, source_dir), # Relative path to temp file
        "-o", os.path.relpath(tex_file, source_dir), # Relative path to output
        "--from", "markdown+wikilinks_title_after_pipe+mark+task_lists+tex_math_dollars",
        "--template", template_arg,
        "--include-before-body", os.path.relpath(cover_tex_path, source_dir),
        "--metadata", f"title={CONFIG['book']['title']}",
        "--metadata", f"subtitle={CONFIG['book']['subtitle']}",
        "--metadata", f"author={CONFIG['book']['author']}",
        "--include-in-header", os.path.relpath(headers_tex_file, source_dir),
        "--include-in-header", callouts_arg,
        "--lua-filter", filter_arg,
        "--syntax-highlighting=tango",
        "--table-of-contents",
        "--toc-depth=4",
        "--number-sections",
        "--top-level-division=chapter",
        "--variable", "book=true",
        "--variable", "strikeout=true",
        "--variable", "classoption=openany", 
        "--variable", "classoption=oneside",
        "--variable", "colorlinks=true", 
        "--variable", f"linkcolor=mylinkcolor",
        "--variable", f"urlcolor=myurlcolor",
        "--standalone"
    ]
    
    if CONFIG['style'].get('mainfont'): cmd_tex.extend(["--variable", f"mainfont={CONFIG['style']['mainfont']}"])
    if CONFIG['style'].get('sansfont'): cmd_tex.extend(["--variable", f"sansfont={CONFIG['style']['sansfont']}"])
    if CONFIG['style'].get('monofont'): cmd_tex.extend(["--variable", f"monofont={CONFIG['style']['monofont']}"])
    if CONFIG['style'].get('geometry'): cmd_tex.extend(["--variable", f"geometry={CONFIG['style']['geometry']}"])
    
    print(f"\nGenerating LaTeX: {tex_file}...\n")
    try:
        # Run in source_dir so that image links "images/..." are found relative to it
        subprocess.run(cmd_tex, check=True, cwd=source_dir)
        print(f"\nDone! {tex_file}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error generating LaTeX: {e}")
        return

    # 2. Compile LaTeX to PDF (xelatex)
    print(f"Compiling PDF from {tex_file} using {pdf_engine}...")
    
    # We need to run xelatex. 
    # If we run from source_dir, we can use -output-directory=artifacts_dir
    # Input file: artifacts_dir/book.tex
    
    tex_cmd = [
        pdf_engine, 
        "-interaction=nonstopmode", 
        f"-output-directory={artifacts_dir_name}",
        os.path.relpath(tex_file, source_dir)
    ]
    
    try:
        print("Pass 1/3 (Init)...")
        # Capture output to silence it, only show on error
        subprocess.run(tex_cmd, check=True, cwd=source_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Pass 2/3 (TOC)...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Pass 3/3 (Refs/MiniTOC)...")
        subprocess.run(tex_cmd, check=True, cwd=source_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error compiling PDF: {e}")
        # Print the captured output for debugging if it failed
        if e.stdout:
            print("\n--- STDOUT ---")
            print(e.stdout.decode('utf-8', errors='ignore'))
        if e.stderr:
            print("\n--- STDERR ---")
            print(e.stderr.decode('utf-8', errors='ignore'))
        print("Check the .log file in artifacts directory for details.")
        return # Stop if failed
        
    # 3. Move PDF to source_dir
    # The pdf will be generated in artifacts_dir with the same basename as tex_file
    generated_pdf = os.path.join(artifacts_dir, output_file)
    final_pdf = os.path.join(source_dir, output_file)
    
    if os.path.exists(generated_pdf):
        shutil.move(generated_pdf, final_pdf)
        print(f"\nDone! Created {final_pdf}")
    else:
        print(f"Error: PDF not found at {generated_pdf}")

    # 4. Cleanup
    cleanup_artifacts(artifacts_dir)
