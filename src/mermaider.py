import os
import re
import hashlib
import subprocess
from .config import CONFIG

def process_mermaid(content: str, source_dir: str) -> str:
    """
    Finds mermaid blocks, generates images using mmdc, and replaces blocks with image links.
    """
    # Regex to find mermaid blocks: ```mermaid ... ```
    pattern = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
    
    # Use images_dir from config or default to source_dir/images
    images_dir_name = CONFIG['resources'].get('images_dir', 'images')
    images_dir = os.path.join(source_dir, images_dir_name)
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    def replacer(match):
        mermaid_code = match.group(1).strip()
        
        # Parse configuration from comments
        # Syntax: %% width=14cm %% or %% height=5cm %% or %% scale=4 %%
        
        # Defaults from config
        width = CONFIG['mermaid'].get('default_width')
        height = CONFIG['mermaid'].get('default_height') or "11cm"
        scale = CONFIG['mermaid'].get('scale', 3.0)
        
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
                # Using shell=True for Windows compatibility with mmdc via cmd /c
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
             # Use relative path for Pandoc
            return f"![\\ ]({images_dir_name}/{image_filename}){{height={height}}}"
        elif width:
            return f"![\\ ]({images_dir_name}/{image_filename}){{width={width}}}"
        else:
            return f"![\\ ]({images_dir_name}/{image_filename})" # Default size

    return pattern.sub(replacer, content)
