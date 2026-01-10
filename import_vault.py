import os
import shutil
import argparse
import re
import sys
import subprocess

def index_attachments(path: str) -> dict[str, str]:
    """Recursively find all files in attachments path."""
    index = {}
    print(f"Indexing attachments in {path}...")
    for root, _, files in os.walk(path):
        for file in files:
            # key is lowercase filename for looser matching
            index[file.lower()] = os.path.join(root, file)
    print(f"Indexed {len(index)} files.\n")
    return index

def import_vault(vault_path: str, attachments_path: str, output_dir: str | None = None) -> tuple[str, str]:
    vault_path = os.path.abspath(vault_path)
    if attachments_path:
        attachments_path = os.path.abspath(attachments_path)
    
    # Derive book name/target dir from folder name if not provided
    base_name = os.path.basename(vault_path.strip(os.sep))
    if not base_name: # Handle root path case
        base_name = "VaultBook"

    target_dir = os.path.abspath(output_dir if output_dir else base_name)
    target_images = os.path.join(target_dir, "images")

    print(f"--- Vault Importer ---")
    print(f"Source: {vault_path}")
    print(f"Attachments: {attachments_path}")
    print(f"Target: {target_dir}")
    print(f"----------------------\n")

    if vault_path == target_dir:
        print("Error: Source and Target directories are the same. Cannot import into self.")
        sys.exit(1)

    # Clean target
    if os.path.exists(target_dir):
        print("Cleaning target directory...\n")
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

    print(f"Copied {len(md_files)} markdown notes.\n")

    # Process Links and Images
    wiki_pattern = re.compile(r'!\[\[(.*?)\]\]')
    std_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    images_copied = set()
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content

        def handle_match(match, link_type):
            if link_type == 'wiki':
                inner = match.group(1)
                parts = inner.split('|')
                fname = parts[0].strip()
            else:
                inner = match.group(1) # alt
                fname = match.group(2).strip() # path
                
            # Finding the file
            base_fname = os.path.basename(fname)
            key = base_fname.lower()
            
            if key in attachment_map:
                src_img = attachment_map[key]
                dest_img = os.path.join(target_images, base_fname)
                
                if base_fname not in images_copied:
                    shutil.copy2(src_img, dest_img)
                    images_copied.add(base_fname)
                
                return f"![](images/{base_fname})"
            else:
                print(f"Warning: Image not found: {fname} in {os.path.basename(md_file)}")
                return match.group(0)

        new_content = wiki_pattern.sub(lambda m: handle_match(m, 'wiki'), new_content)
        new_content = std_pattern.sub(lambda m: handle_match(m, 'std'), new_content)

        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"Processed {len(images_copied)} unique images.\n")

    return target_dir, base_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import Obsidian vault and build PDF book.")
    parser.add_argument("--source", "-s", required=True, help="Path to the source Obsidian vault folder (e.g. 'E:/Obsidian/Java')")
    parser.add_argument("--attachments", "-a", required=True, help="Path to the global Attachments folder")
    parser.add_argument("--output", "-o", help="Name of the output build directory (defaults to source folder name)")
    parser.add_argument("--build", "-b", action="store_true", help="Trigger build_book.py after import")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.source):
        print(f"Error: Vault path does not exist: {args.source}")
        sys.exit(1)
    if not os.path.isdir(args.attachments):
        print(f"Error: Attachments path does not exist: {args.attachments}")
        sys.exit(1)
        
    target_dir, book_title = import_vault(args.source, args.attachments, args.output)
    
    if args.build:
        print("\n--- Starting Build Process ---\n")
        # Override config by setting env vars, implementing user request:
        # "book title will always be the same as the source dir for now"
        os.environ["SOURCE_DIR"] = target_dir
        os.environ["BOOK_TITLE"] = book_title
        os.environ["OUTPUT_FILE"] = f"{book_title}.pdf"
        
        try:
            # Dynamic import to ensure config picks up the new env vars
            from src.builder import build
            build()
            print(f"\nSUCCESS: Book built at {target_dir}/{book_title}.pdf")
        except Exception as e:
            print(f"\nFAILURE: Build failed with error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
