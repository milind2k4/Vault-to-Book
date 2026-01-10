import sys
import os

# Add project root to sys.path so we can import 'src'
sys.path.append(os.getcwd())

try:
    from src.builder import build
    # No environment variables set here.
    # We rely entirely on config.yaml being present and correct.
    print("Starting build using settings from config.yaml...")
    build()
    print("Build complete.")
except ImportError as e:
    print(f"Import Error: {e}")
    print("Ensure you are running this script from the project root.")
except Exception as e:
    print(f"Build Failed: {e}")
    import traceback
    traceback.print_exc()
