import os
import shutil
import argparse
import re
import subprocess
import glob
import sys

def index_attachments(path):
    """Recursively find all files in attachments path."""
    index = {}
    print(f"Indexing attachments in {path}...")
    for root, _, files in os.walk(path):
        for file in files:
            # key is lowercase filename for looser matching
            index[file.lower()] = os.path.join(root, file)
    print(f"Indexed {len(index)} files.")
    return index

def import_vault(vault_path, attachments_path):
    vault_path = os.path.abspath(vault_path)
    if attachments_path:
        attachments_path = os.path.abspath(attachments_path)
    
    # Derive book name from folder name
    base_name = os.path.basename(vault_path.strip(os.sep))
    if not base_name: # Handle root path case
        base_name = "VaultBook"

    target_dir = os.path.abspath(base_name)
    target_images = os.path.join(target_dir, "images")

    print(f"--- Vault Importer ---")
    print(f"Source: {vault_path}")
    print(f"Attachments: {attachments_path}")
    print(f"Target: {target_dir}")
    print(f"----------------------")

    if vault_path == target_dir:
        print("Error: Source and Target directories are the same. Cannot import into self.")
        sys.exit(1)

    # Clean target
    if os.path.exists(target_dir):
        print("Cleaning target directory...")
        shutil.rmtree(target_dir)
    os.makedirs(target_images, exist_ok=True)

    # Index attachments
    attachment_map = index_attachments(attachments_path)

    # Scan and Copy MD files
    md_files = []
    print("Scanning vault for markdown files...")
    for root, dirs, files in os.walk(vault_path):
        # Skip hidden folders
        if '.obsidian' in dirs: dirs.remove('.obsidian')
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            if file.lower().endswith(".md"):
                src = os.path.join(root, file)
                # Flatten structure
                dest = os.path.join(target_dir, file)
                shutil.copy2(src, dest)
                md_files.append(dest)

    print(f"Copied {len(md_files)} markdown notes.")

    # Process Links and Images
    # Matches ![[image.png]] or ![[image.png|size]]
    # Matches ![](image.png)
    wiki_pattern = re.compile(r'!\[\[(.*?)\]\]')
    std_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    images_copied = set()
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content

        def handle_match(match, link_type):
            if link_type == 'wiki':
                # content inside [[ ]] could be 'Image.png|100'
                inner = match.group(1)
                parts = inner.split('|')
                fname = parts[0].strip()
            else:
                # std link: ![alt](path)
                inner = match.group(1) # alt
                fname = match.group(2).strip() # path
                
            # Finding the file
            # Remove any directory prefix from fname (if user had path/to/img)
            base_fname = os.path.basename(fname)
            key = base_fname.lower()
            
            if key in attachment_map:
                src_img = attachment_map[key]
                dest_img = os.path.join(target_images, base_fname)
                
                if base_fname not in images_copied:
                    shutil.copy2(src_img, dest_img)
                    images_copied.add(base_fname)
                
                # Rewrite link to relative path
                return f"![](images/{base_fname})"
            else:
                print(f"Warning: Image not found: {fname} in {os.path.basename(md_file)}")
                return match.group(0) # Keep original if not found

        # Replace Wiki Links
        new_content = wiki_pattern.sub(lambda m: handle_match(m, 'wiki'), new_content)
        # Replace Std Links
        new_content = std_pattern.sub(lambda m: handle_match(m, 'std'), new_content)

        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"Processed {len(images_copied)} unique images.")

    # Run Build
    print("\n--- Starting Build Process ---\n")
    
    env = os.environ.copy()
    env["SOURCE_DIR"] = base_name
    env["BOOK_TITLE"] = base_name
    env["BOOK_SUBTITLE"] = "Personal Notes" # Default or customizable?
    env["OUTPUT_FILE"] = f"{base_name}.pdf"
    
    # Check for logo
    # If logo.png exists in copied images, good.
    # build_book.py expects SOURCE_DIR/images/logo.png
    if "logo.png" not in images_copied:
        print("Warning: 'logo.png' not found in attachments. Cover page might miss logo.")
    
    try:
        subprocess.run(["python", "build_book.py"], env=env, check=True)
        print(f"\nSUCCESS: Book built at {base_name}.pdf")
    except subprocess.CalledProcessError:
        print("\nFAILURE: Build script failed.")
        sys.exit(1)

# --- Configuration ---
# Update these paths to point to your Obsidian vault and attachments folder
VAULT_PATH = r"E:\Obsidian\College\DBMS"  # Example Path
ATTACHMENTS_PATH = r"E:\Obsidian\00 Attachments" # Example Path
# ---------------------

if __name__ == "__main__":
    if not os.path.isdir(VAULT_PATH):
        print(f"Error: Vault path does not exist: {VAULT_PATH}")
        sys.exit(1)
    if not os.path.isdir(ATTACHMENTS_PATH):
        print(f"Error: Attachments path does not exist: {ATTACHMENTS_PATH}")
        sys.exit(1)
        
    import_vault(VAULT_PATH, ATTACHMENTS_PATH)
