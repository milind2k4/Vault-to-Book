import os
import re
import subprocess
import datetime

# --- CONFIGURATION ---
# The script will ask for the Subject Name (e.g., "Core Java") to name the file and title page.
TEMPLATE_FILENAME = "eisvogel.latex" 
AUTHOR_NAME = "Milind"  # Change this to your name
# ---------------------

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text

def convert_images(text):
    """
    Converts Obsidian ![[image.png]] to standard Markdown ![image](image.png)
    Also handles resized images ![[image.png|100]] -> ![image](image.png) (ignoring size for now or could use pandoc attrs)
    """
    # Pattern: ![[filename(|resize)?]]
    # Replacement: ![filename](filename)
    
    def replace_image(match):
        content = match.group(1)
        if "|" in content:
            filename, _ = content.split("|", 1)
        else:
            filename = content
            
        return f"![{filename}]({filename})"

    return re.sub(r'!\[\[(.*?)\]\]', replace_image, text)

def convert_callouts(text):
    """
    Converts Obsidian > [!TIP] to LaTeX colored boxes.
    """
    colors = {
        "NOTE": "blue",
        "TIP": "teal",
        "WARNING": "red",
        "ERROR": "red",
        "EXAMPLE": "gray",
        "QUOTE": "violet"
    }

    def replace_block(match):
        callout_type = match.group(1).upper()
        title = match.group(2).strip() if match.group(2) else callout_type.title()
        # Escape special LaTeX characters in the title
        title = title.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_').replace('$', '\\$').replace('#', '\\#')
        
        content = match.group(3)
        
        color = colors.get(callout_type, "gray")
        
        # Eisvogel specific tcolorbox formatting
        latex_start = f'\\begin{{tcolorbox}}[colback={color}!5!white,colframe={color}!75!black,title={title}]'
        latex_end = '\\end{tcolorbox}'
        
        # Use Pandoc's raw_attribute extension to inject LaTeX commands
        # The content remains outside the raw blocks so it's processed as Markdown
        return f"\n```{{=latex}}\n{latex_start}\n```\n{content}\n```{{=latex}}\n{latex_end}\n```\n"

    pattern = r'>\s*\[!(\w+)\]\s*(.*?)\n((?:>.*\n?)*)'
    return re.sub(pattern, replace_block, text, flags=re.MULTILINE)

def convert_wikilinks(text, all_filenames):
    """
    Converts [[Note Name]] to [Note Name](#note-name)
    """
    def replace_link(match):
        content = match.group(1)
        if "|" in content:
            target, alias = content.split("|", 1)
        else:
            target, alias = content, content

        if "#" in target:
            target_file, heading = target.split("#", 1)
            # If target_file is empty (e.g. [[#Heading]]), we link to current doc's heading
            # But in merged master, uniqueness is tricky. Assuming standard usage.
            slug = slugify(heading)
        else:
            slug = slugify(target)
            
        return f"[{alias}](#{slug})"

    return re.sub(r'\[\[(.*?)\]\]', replace_link, text)

def generate_mini_toc(text):
    toc_lines = ["\n**Topics in this chapter:**\n"]
    headers = re.findall(r'^##\s+(.+)$', text, re.MULTILINE)
    if not headers: return ""
    for h in headers:
        slug = slugify(h)
        toc_lines.append(f"- [{h}](#{slug})")
    return "\n".join(toc_lines) + "\n\n"

def main():
    # 1. Setup
    subject = "Java"
    output_filename = f"{subject}.pdf"
    
    notes_dir = subject
    files = sorted([os.path.join(notes_dir, f) for f in os.listdir(notes_dir) if f.endswith('.md') and f != "temp_master.md"])
    if not files:
        print("No markdown files found!")
        return

    # 2. Create the YAML Metadata for the Cover Page
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    # 2. Create the YAML Metadata for the Cover Page
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    # Part 1: Dynamic metadata (safe for f-string)
    yaml_head = f"""---
title: "{subject}"
author: "{AUTHOR_NAME}"
date: "{current_date}"
titlepage: true
titlepage-color: "06386e" 
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
toc-own-page: true
"""

    # Part 2: Static LaTeX definitions (raw string to handle backslashes and braces safe)
    # properly indented to match line start if needed, but YAML is sensitive.
    # We'll just append it.
    yaml_tail = r"""header-includes:
  - \usepackage{tcolorbox}
  - \usepackage{xcolor}
  - \definecolor{titlepage-color}{HTML}{06386e}
  - \definecolor{tiplight}{HTML}{E0F7FA}
  - \definecolor{tipdark}{HTML}{006064}
  - \definecolor{notelight}{HTML}{E3F2FD}
  - \definecolor{notedark}{HTML}{0D47A1}
  - \definecolor{warninglight}{HTML}{FFEBEE}
  - \definecolor{warningdark}{HTML}{B71C1C}
...
"""
    
    master_content = yaml_head + yaml_tail + "\n"
    # Note: "06386e" is a nice academic blue. You can change the hex code.

    print(f"Found {len(files)} notes. Processing...")

    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Remove existing YAML (--- ... ---) from individual notes so they don't break the book
            content = re.sub(r'^---[\s\S]*?---\n', '', content)
            
            # Convert Filename to H1
            title = filename.replace(".md", "")
            h1_header = f"# {title}\n"
            
            # Add Mini TOC
            mini_toc = generate_mini_toc(content)
            
            # Process content
            content = convert_images(content)
            content = convert_callouts(content)
            
            master_content += f"\n{h1_header}\n{mini_toc}\n{content}\n\\newpage\n"

    master_content = convert_wikilinks(master_content, files)

    with open("temp_master.md", "w", encoding='utf-8') as f:
        f.write(master_content)

    # 3. Run Pandoc
    print("Generating PDF... (This might take a minute)")
    
    # We use the full path to the local template file
    cmd = [
        "pandoc", "temp_master.md",
        "-o", output_filename,
        "--from", "markdown",
        f"--template={TEMPLATE_FILENAME}",
        "--syntax-highlighting=idiomatic",
        "--toc",
        "--number-sections"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Success! Created: {output_filename}")
    except subprocess.CalledProcessError as e:
        print("❌ Error. Check if you have LaTeX installed and 'eisvogel.latex' is in this folder.")
        print(f"Error details: {e}")

    if os.path.exists("temp_master.md"):
        os.remove("temp_master.md")

if __name__ == "__main__":
    main()