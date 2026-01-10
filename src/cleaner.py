import os
import glob
from .config import CONFIG

def cleanup_artifacts(artifacts_dir: str) -> None:
    """
    Deletes temporary LaTeX build artifacts from the artifacts directory.
    Keeps .log, .tex, and .md for debugging since they are isolated now.
    """
    print(f"\nCleaning up artifacts in {artifacts_dir}...")
    
    # Extensions to delete (keeping .maf temporarily for debug)
    extensions_to_delete = [
        ".aux", ".toc", ".out", 
        ".fls", ".fdb_latexmk", ".synctex.gz"
    ]
    
    count = 0
    
    # 1. Delete extension-based files
    for ext in extensions_to_delete:
        files = glob.glob(os.path.join(artifacts_dir, f"*{ext}"))
        for f in files:
            try:
                os.remove(f)
                count += 1
            except OSError as e:
                print(f"Error deleting {f}: {e}")

    # 2. Delete .mtc files (mtc, mtc0, mtc1...)
    # Disabled for MiniTOC debugging
    # mtc_files = glob.glob(os.path.join(artifacts_dir, "*.mtc*"))
    # for f in mtc_files:
    #     try:
    #         os.remove(f)
    #         count += 1
    #     except OSError as e:
    #         print(f"Error deleting {f}: {e}")

    print(f"Cleanup: Removed {count} temporary files from {os.path.basename(artifacts_dir)}.")
    print("Kept .tex, .log, and temp_master.md for debugging.")
