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
    
    # Prepare Image Defaults
    img_conf = CONFIG.get('images', {})
    img_opts = []
    if img_conf.get('max_width'):
        img_opts.append(f"max width={img_conf['max_width']}")
    if img_conf.get('max_height'):
        img_opts.append(f"max height={img_conf['max_height']}")
    if img_conf.get('keep_aspect_ratio', True):
        img_opts.append("keepaspectratio")
    
    opts = ",".join(img_opts)
    
    # --- Configuration Preparation ---
    table_conf = CONFIG.get('tables', {})
    row_colors_tex = ""
    if table_conf.get('row_colors', True):
        odd = table_conf.get('odd_color', 'white')
        even = table_conf.get('even_color', 'RoyalBlue!20')
        row_colors_tex = f"\\rowcolors{{2}}{{{even}}}{{{odd}}}"
    
    table_stretch = table_conf.get('stretch', 1.2)
    
    headers_tex_content = f"""
\\usepackage{{caption}}
\\captionsetup[figure]{{labelsep=none, justification=centering}}

\\usepackage{{etoc}} 

\\usepackage[version=4]{{mhchem}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{mathtools}}
\\usepackage{{gensymb}}
\\usepackage{{cancel}}

\\usepackage[export]{{adjustbox}} % For max width=... in includegraphics
\\usepackage{{float}} % Required for [H] figure placement

% --- Global Image Sizing from Config ---
\\makeatletter
\\let\\oldincludegraphics\\includegraphics
\\renewcommand{{\\includegraphics}}[2][]{{
  \\oldincludegraphics[{opts},#1]{{#2}}
}}
\\makeatother
% \\mtcselectlanguage{{english}} - Removed
\\definecolor{{mylinkcolor}}{{HTML}}{{{link_color}}}
\\definecolor{{myurlcolor}}{{HTML}}{{{url_color}}}
% --- Chapter Title Styling (KOMA-Script) ---
\\renewcommand*\\chapterformat{{\\thechapter.\\enskip}}
\\addtokomafont{{chapter}}{{\\centering}}
\\RedeclareSectionCommand[beforeskip={top_margin},afterskip={bottom_margin}]{{chapter}}

% --- Table Styling ---
{row_colors_tex}
\\renewcommand{{\\arraystretch}}{{{table_stretch}}}

% --- Heading Styling ---
\\makeatletter
\\renewcommand\\sectionlinesformat[4]{{%
  \\ifstr{{#1}}{{section}}{{%
    \\vspace{{0.2em}}
    \\rule{{\\linewidth}}{{0.5pt}}\\par\\nobreak\\nointerlineskip
    \\@hangfrom{{\\hskip #2#3}}{{#4}}\\par\\nobreak\\nointerlineskip
    \\vspace{{0.1em}}
    \\rule{{\\linewidth}}{{0.5pt}}\\par
  }}{{%
    \\@hangfrom{{\\hskip #2#3}}{{#4}}%
  }}%
}}
\\makeatother
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
    
    # Logic to find logo: source_dir/images/logo.png
    # output_dir is inside source_dir/build_artifacts, so parent is source_dir
    source_dir = os.path.dirname(output_dir)
    
    images_dir_name = CONFIG['resources'].get('images_dir', 'images')
    logo_file_path = os.path.join(source_dir, images_dir_name, "logo.png")
    
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
"""
    cover_tex_path = os.path.join(output_dir, "cover.tex")
    with open(cover_tex_path, 'w', encoding='utf-8') as f:
        f.write(cover_content)
    return cover_tex_path
