# Build Process Execution Flow

This diagram illustrates the workflow using the `main.py` script, which handles importing, building, and cleanup.

```mermaid
graph LR
    User([User])
    EntryScript["main.py"]
    Config["src/config.py"]
    Builder["src/builder.py"]
    TexManager["src/tex_manager.py"]
    Mermaider["src/mermaider.py"]
    Cleaner["src/cleaner.py"]
    Pandoc[["Pandoc Exec"]]
    XeLaTeX[["XeLaTeX Exec"]]
    
    subgraph LuaFilters [Lua Filters]
        Chemistry("chemistry.lua")
        Tables("tables.lua")
        Images("images.lua")
        Links("links.lua")
        Callouts("callouts.lua")
        Typography("typography.lua")
    end
    
    ConfigYAML[("config.yaml")]
    RawNotes[("Obsidian Notes")]
    RawAttachments[("Attachments")]
    ImportDir[("Import Directory")]
    TempMaster[("book_master.md")]
    TeX_File[("book.tex")]
    PDF_File[("book.pdf")]
    ImagesArtifacts[("Diagram Images")]
    ArtifactsDir{"build_artifacts/"}
    FinalOutput[("Final PDF Output")]

    User -->|Run CLI| EntryScript
    EntryScript -->|Copy| RawNotes
    EntryScript -->|Copy| RawAttachments
    EntryScript -->|Create| ImportDir
    
    EntryScript -->|Set Env Vars| Config
    Config -->|Load Defaults/File| ConfigYAML
    
    EntryScript -->|Call build| Builder
    
    subgraph BuilderLogic [Builder Execution]
        Builder -->|Ensure Dir| ArtifactsDir
        Builder -->|Scan| ImportDir
        
        Builder -->|generate_headers_tex| TexManager
        Builder -->|generate_cover_tex| TexManager
        
        Builder -->|process_file| Builder
        Builder -->|process_mermaid| Mermaider
        Mermaider -->|Generate| ImagesArtifacts
        
        Builder -->|Write| TempMaster
        
        Builder -->|Subprocess Call| Pandoc
        Pandoc -.->|Uses| LuaFilters
        Pandoc -.->|Reads| TempMaster
        Pandoc -->|Generates| TeX_File
        
        Builder -->|Subprocess Call x3| XeLaTeX
        XeLaTeX -.->|Reads| TeX_File
        XeLaTeX -->|Generates| PDF_File
    end
    
    EntryScript -->|Cleanup Strategy| Cleaner
    
    Cleaner -->|Option: none| KeepAll[Keep All Files]
    Cleaner -->|Option: latex| DelIntermediates[Delete .aux .toc etc]
    Cleaner -->|Option: artifacts| DelArtifacts[Delete build_artifacts Folder]
    
    EntryScript -->|Option: strict| StrictCleanup
    StrictCleanup -->|Move| PDF_File
    StrictCleanup --> FinalOutput
    StrictCleanup -->|Delete| ImportDir
```

## Workflow Steps

1.  **Import & Setup**: 
    -   `main.py` accepts arguments for vault path, attachments, title, author, etc.
    -   It copies valid notes and attachments to a clean import directory.
    -   It sets environment variables to override default configuration.

2.  **Build Execution**:
    -   The script invokes `src.builder.build()`.
    -   Markdown files are processed (Mermaid generation, header fixing).
    -   Pandoc converts the content to LaTeX using a chain of modular Lua filters (`chemistry`, `tables`, `images`, `callouts`, `links`, `typography`).
    -   XeLaTeX compiles the PDF (3 passes for correct TOC/references).

3.  **Cleanup**:
    -   Based on the `--cleanup` argument:
        -   `latex`: Removes temporary LaTeX files (`.aux`, `.log` is kept).
        -   `artifacts`: Removes the entire `build_artifacts` folder.
        -   `strict`: Moves the final PDF to the user-specified location and deletes the *entire* import directory (source copies + build artifacts).
