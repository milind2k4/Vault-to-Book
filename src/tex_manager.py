import os
from datetime import date
from .config import CONFIG

def generate_headers_tex(output_dir: str) -> str:
    """
    Generates the headers.tex file used for LaTeX configuration.
    """
    link_color = CONFIG['style']['link_color']
    url_color = CONFIG['style']['url_color']
    top_margin = CONFIG['style']['chapter_title_top_margin']
    bottom_margin = CONFIG['style']['chapter_title_bottom_margin']
    
    headers_tex_content = f"""
\\usepackage{{caption}}
\\captionsetup[figure]{{labelsep=none, justification=centering}}
\\usepackage{{etoc}} % Replaces minitoc
\\usepackage[version=4]{{mhchem}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{mathtools}}
\\usepackage{{gensymb}}
\\usepackage[export]{{adjustbox}} % For max width=... in includegraphics
\\usepackage{{cancel}}
% \\mtcselectlanguage{{english}} - Removed
\\definecolor{{mylinkcolor}}{{HTML}}{{{link_color}}}
\\definecolor{{myurlcolor}}{{HTML}}{{{url_color}}}
% --- Chapter Title Styling (KOMA-Script) ---
\\renewcommand*\\chapterformat{{\\thechapter.\\enskip}}
\\addtokomafont{{chapter}}{{\\centering}}
\\RedeclareSectionCommand[beforeskip={top_margin},afterskip={bottom_margin}]{{chapter}}
% --- Table Styling ---
\\rowcolors{{2}}{{RoyalBlue!20}}{{white}}
\\renewcommand{{\\arraystretch}}{{1.2}}
% -------------------------------------------
"""
    headers_tex_file = os.path.join(output_dir, "headers.tex")
    with open(headers_tex_file, 'w', encoding='utf-8') as f:
        f.write(headers_tex_content)
    return headers_tex_file

def generate_cover_tex(output_dir: str) -> str:
    """
    Generates the cover.tex file.
    """
    book_title = CONFIG['book']['title']
    book_subtitle = CONFIG['book']['subtitle']
    book_author = CONFIG['book']['author']
    current_date = date.today().strftime("%B %d, %Y")
    
    # Logic to find logo: It's usually in source_dir/images/logo.png
    # But output_dir is source_dir/build_artifacts
    # So we should check parent of output_dir for images?
    # Or rely on Config?
    
    # We can infer source_dir from output_dir if assume standard structure
    # output_dir = source_dir/build_artifacts
    # source_dir = output_dir/..
    source_dir = os.path.dirname(output_dir)
    
    images_dir_name = CONFIG['resources'].get('images_dir', 'images')
    logo_file_path = os.path.join(source_dir, images_dir_name, "logo.png")
    
    # For LaTeX, we need a path relative to where compilation happens (source_dir)
    # OR an absolute path ( safest)
    # Let's use absolute path for the image inclusion to be safe
    # REPLACE BACKSLASHES for LaTeX
    logo_tex_path = logo_file_path.replace("\\", "/")
    
    # Conditional Logo
    logo_block = ""
    if os.path.exists(logo_file_path):
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
    {{\\fontsize{{50}}{{60}}\\selectfont \\bfseries {book_title} \\par}}
    \\vspace{{1cm}}
    {{\\fontsize{{20}}{{30}}\\selectfont {book_subtitle.replace("&", "\\&")} \\par}}
    
    \\vfill
    
    {{\\fontsize{{18}}{{22}}\\selectfont {book_author} \\par}}
    \\vspace{{0.5cm}}
    {{\\large {current_date} \\par}}
    
    \\vspace{{3cm}}
    \\restoregeometry
\\end{{titlepage}}

% Initialize MiniTOC (Removed, using etoc)
"""
    cover_tex_path = os.path.join(output_dir, "cover.tex")
    with open(cover_tex_path, 'w', encoding='utf-8') as f:
        f.write(cover_content)
    return cover_tex_path
