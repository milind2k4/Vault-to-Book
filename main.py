import os
import shutil
import argparse
import re
import sys
import pickle
import time

# Add project root to sys.path so we can import 'src'
sys.path.append(os.getcwd())

from src.builder import build
from src.cleaner import cleanup_artifacts
from src.config import CONFIG
from src.colors import Colors


CACHE_FILE = ".attachments_index.pkl"
CACHE_EXPIRY_SECONDS = 24 * 60 * 60  # 24 hours

def index_attachments(path: str) -> dict[str, str]:
    """
    Recursively find all files in attachments path.
    Uses a pickle cache to speed up subsequent runs.
    """
    if not os.path.exists(path):
        return {}

    # Check cache
    if os.path.exists(CACHE_FILE):
        last_modified = os.path.getmtime(CACHE_FILE)
        if time.time() - last_modified < CACHE_EXPIRY_SECONDS:
            print(Colors.info("Loading attachment index from cache..."))
            try:
                with open(CACHE_FILE, 'rb') as f:
                    index = pickle.load(f)
                print(Colors.info(f"Loaded {len(index)} files from cache.\n"))
                return index
            except Exception as e:
                print(Colors.warning(f"Failed to load cache: {e}. Re-indexing."))
    
    # Re-index
    index = {}
    print(Colors.info(f"Indexing attachments in {path}..."))
    for root, _, files in os.walk(path):
        for file in files:
            # key is lowercase filename for looser matching
            index[file.lower()] = os.path.join(root, file)
    
    # Save cache
    try:
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(index, f)
        print(Colors.info(f"Saved index to cache ({len(index)} files).\n"))
    except Exception as e:
        print(Colors.warning(f"Failed to save cache: {e}"))
        
    return index

def import_vault(vault_path: str, attachments_path: str, output_dir: str) -> str:
    """
    Imports notes and attachments to output_dir.
    Returns the absolute path to the prepared output directory.
    """
    vault_path = os.path.abspath(vault_path)
    if attachments_path:
        attachments_path = os.path.abspath(attachments_path)
    
    target_dir = os.path.abspath(output_dir)
    target_images = os.path.join(target_dir, "images")

    print(Colors.section("Vault Importer"))
    print(f"Source: {Colors.BOLD}{vault_path}{Colors.ENDC}")
    print(f"Attachments: {Colors.BOLD}{attachments_path}{Colors.ENDC}")
    print(f"Target: {Colors.BOLD}{target_dir}{Colors.ENDC}")
    print(f"----------------------\n")

    if vault_path == target_dir:
        print(Colors.error("Error: Source and Target directories are the same. Cannot import into self."))
        sys.exit(1)

    # Clean target
    if os.path.exists(target_dir):
        print(Colors.info("Cleaning target directory...\n"))
        try:
            shutil.rmtree(target_dir)
        except Exception as e:
            print(Colors.warning(f"Warning: Failed to clean target directory: {e}. Trying to proceed."))
    
    os.makedirs(target_images, exist_ok=True)

    # Index attachments
    attachment_map = index_attachments(attachments_path)

    # Scan and Copy MD files
    md_files = []
    print(Colors.info("Scanning vault for markdown files..."))
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

    print(Colors.info(f"Copied {len(md_files)} markdown notes.\n"))

    # Process Links and Images
    wiki_pattern = re.compile(r'!\[\[(.*?)\]\]')
    std_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    images_copied = set()
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content

        def handle_match(match: re.Match, link_type: str) -> str:
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
                return match.group(0)

        new_content = wiki_pattern.sub(lambda m: handle_match(m, 'wiki'), new_content)
        new_content = std_pattern.sub(lambda m: handle_match(m, 'std'), new_content)

        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    print(f"Processed {len(images_copied)} unique images.\n")

    return target_dir

def main():
    parser = argparse.ArgumentParser(description="Import Obsidian vault and build PDF book.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("notes_dir", help="Path to the source Obsidian vault folder")
    parser.add_argument("attachments_dir", help="Path to the global Attachments folder")
    
    # Optional arguments that derive defaults or have defaults
    parser.add_argument("--title", "-t", help="Book title (defaults to notes_dir name)")
    parser.add_argument("--subtitle", "-s", default="Personal Notes and References", help="Book subtitle")
    parser.add_argument("--author", "-a", default="Anonymous", help="Book author")
    
    parser.add_argument("--cleanup", "-c", choices=["none", "latex", "artifacts", "strict"], default="latex",
                        help="Cleanup strategy: 'latex' (del intermediates), 'artifacts' (del build folder), 'strict' (del everything, move pdf), 'none' (keep all)")
    
    parser.add_argument("--output-pdf", "-o", help="Specific output path for PDF (Required for 'strict' cleanup if you want to save the PDF)")
    parser.add_argument("--build-path", "-bp", help="Directory where the build will take place (defaults to 'title')")

    args = parser.parse_args()
    
    # 1. Validation
    if not os.path.isdir(args.notes_dir):
        print(f"Error: Notes directory does not exist: {args.notes_dir}")
        sys.exit(1)
    if not os.path.isdir(args.attachments_dir):
        print(f"Error: Attachments directory does not exist: {args.attachments_dir}")
        sys.exit(1)

    # 2. Defaults
    if not args.title:
        # Use directory name of inputs
        args.title = os.path.basename(os.path.abspath(args.notes_dir))
    
    print(f"\nBuild Configuration:")
    print(f"  Title:    {args.title}")
    print(f"  Subtitle: {args.subtitle}")
    print(f"  Author:   {args.author}")
    print(f"  Cleanup:  {args.cleanup}")
    
    # 3. Import   
    safe_import_dir = args.build_path if args.build_path else args.title
    absolute_source = os.path.abspath(args.notes_dir)
    absolute_target = os.path.abspath(safe_import_dir)
    
    if absolute_source == absolute_target:
        print(f"Notice: Output directory '{safe_import_dir}' conflicts with source. using '{safe_import_dir}_build' instead.")
        safe_import_dir = f"{safe_import_dir}_build"
    
    # 4. Configure & Build
    
    output_filename = f"{args.title}.pdf"
    
    try:
        # Perform Import
        import_dir = import_vault(args.notes_dir, args.attachments_dir, safe_import_dir)
        
        # Update Global Config
        CONFIG['build']['source_dir'] = import_dir
        CONFIG['build']['output_file'] = output_filename
        CONFIG['book']['title'] = args.title
        CONFIG['book']['subtitle'] = args.subtitle
        CONFIG['book']['author'] = args.author

        print(Colors.section("Starting Build Process"))
        build()
        
        # Verify if PDF exists
        final_pdf_path = os.path.join(import_dir, output_filename)
        if not os.path.exists(final_pdf_path):
            print(Colors.error(f"\nError: Expected PDF not found at {final_pdf_path}. Build likely failed."))
            sys.exit(1)
            
        print(Colors.success(f"SUCCESS: Book built at {final_pdf_path}"))
        
        # Move PDF if output_pdf is specified (For ANY cleanup mode)
        if args.output_pdf:
            dest_pdf = os.path.abspath(args.output_pdf)
             # If target directory doesn't exist, create it
            dest_dir = os.path.dirname(dest_pdf)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # If user specified a directory (ends with slash or exists as dir), handle that
            if os.path.isdir(dest_pdf):
                 dest_pdf = os.path.join(dest_pdf, output_filename)
            
            # If cleanup is strict, we MUST move it out because build dir is deleted.
            # If cleanup is NOT strict, user expects it in build_path (per requirements)
            if args.cleanup != "strict":
                shutil.copy2(final_pdf_path, dest_pdf)
                # final_pdf_path remains pointing to the build_dir version for logging if needed
                # or strictly speaking, we validly created dest_pdf too.
                pass
            else:
                shutil.move(final_pdf_path, dest_pdf)
                final_pdf_path = dest_pdf
                
            print(Colors.info(f"PDF Output: {dest_pdf}"))
        
        # 5. Cleanup
        # Define artifacts dir location (inside import_dir/build_artifacts by default)
        artifacts_dir = os.path.join(import_dir, "build_artifacts")
        
        if args.cleanup == "none":
            print(Colors.info("Cleanup: none selected. Keeping all files."))
            
        elif args.cleanup == "latex":
            # This deletes .aux, .toc etc but keeps logs and tex
            cleanup_artifacts(artifacts_dir)
            print(Colors.info("Cleanup: Removed intermediate LaTeX files."))
            
        elif args.cleanup == "artifacts":
            if os.path.exists(artifacts_dir):
                shutil.rmtree(artifacts_dir)
                print(Colors.info(f"Cleanup: Removed artifacts directory: {artifacts_dir}"))
                
        elif args.cleanup == "strict":            
            if not args.output_pdf:
                 # Default output was current dir
                 dest_pdf = os.path.abspath(output_filename)
                 if final_pdf_path != dest_pdf:
                     if os.path.exists(final_pdf_path): # Check if it's still there (might be same path)
                        shutil.move(final_pdf_path, dest_pdf)
                        print(Colors.info(f"Moved PDF to: {dest_pdf}"))
            
            # Delete the ENTIRE import directory
            if os.path.exists(import_dir):
                shutil.rmtree(import_dir)
                print(Colors.info(f"Cleanup: Removed build directory: {import_dir}"))

    except ImportError as e:
         print(Colors.error(f"Error importing modules: {e}"))
         print("Make sure you are running from the project root.")
         sys.exit(1)
    except Exception as e:
        print(Colors.error(f"\nFAILURE: Build failed with error: {e}"))
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
