import os
import glob

def cleanup_artifacts(artifacts_dir: str) -> None:
    """
    Deletes temporary LaTeX build artifacts from the artifacts directory.
    Keeps .log, .tex, and .md for debugging.
    """
    print(f"\nCleaning up artifacts in {artifacts_dir}...")
    
    extensions_to_delete = [
        ".aux", ".toc", ".out", 
        ".fls", ".fdb_latexmk", ".synctex.gz"
    ]
    
    count = 0
    
    for ext in extensions_to_delete:
        files = glob.glob(os.path.join(artifacts_dir, f"*{ext}"))
        for f in files:
            try:
                os.remove(f)
                count += 1
            except OSError as e:
                print(f"Error deleting {f}: {e}")

    # Delete .mtc files if present (legacy)
    # Was used when we were using MiniTOC
    mtc_files = glob.glob(os.path.join(artifacts_dir, "*.mtc*"))
    for f in mtc_files:
         try:
             os.remove(f)
             count += 1
         except OSError:
             pass

    print(f"Cleanup: Removed {count} temporary files from {os.path.basename(artifacts_dir)}.")
