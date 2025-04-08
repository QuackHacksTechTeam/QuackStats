
LINE_THRESHOLD = 2000 
EXCLUDED_PATHS = [
    "node_modules",  # Node.js dependencies
    "dist",           # Distribution files
    "build",          # Build directory
    "out",            # Output files
    "bin",            # Binary files
    ".git",           # Git internal metadata
    ".github",        # GitHub-specific configuration
    ".vscode",        # VSCode-specific settings
    "__pycache__",
    "bower_components",  # Bower dependencies
    "pip-cache",      # Python pip cache
    "tmp",            # Temporary files
    "temp",           # Temporary files
    "*.log",          # Log files
    "*.bak",          # Backup files
    "*.swp",          # Vim swap files
    "docs",           # Documentation directory
    "README.md",      # Documentation file
    ".idea",          # JetBrains project files
    ".project",       # Eclipse project file
    ".settings",      # Eclipse settings
    ".DS_Store",      # macOS system files
    "Thumbs.db",      # Windows system files
    "*.exe", "*.dll", "*.pdb",  # Executables and binaries
    ".env",           # Environment variables
    "*.sqlite", "*.db"  # Database files
]

INCLUDED_EXTENSIONS = [
    # General Purpose Languages
    ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".cs", ".java", ".py",
    ".js", ".mjs", ".cjs", ".ts", ".tsx", ".go", ".rs", ".swift", ".kt", ".kts", ".dart",
    
    # Web Development
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".php", ".rb", ".aspx", ".cshtml",
    ".twig", ".liquid",

    # Shell and Scripting
    ".sh", ".ps1", ".psm1", ".bat", ".cmd", ".pl", ".perl",

    # Data Science & Config
    ".r", ".jl", ".ipynb",

    # Low-Level & Embedded
    ".asm", ".s", ".v", ".sv", ".vhdl", ".ino",

    # Database & Query
    ".sql", ".psql",

    # Functional Languages
    ".hs", ".lhs", ".ml", ".mli", ".fs", ".fsi", ".fsx", ".clj", ".cljs", ".edn", ".lisp", ".scm", ".rkt",

    # Misc
    ".lua", ".coffee"
]


def is_excluded_file(file) -> bool: 
    """
    Used to check if a file commitment was likely to come from a 
    source that should not contribute to line count, e.g. pushing node modules 
    """

    if file.additions + file.deletions > LINE_THRESHOLD: 
        return True 

    if any(excluded_path in file.filename for excluded_path in EXCLUDED_PATHS):
        return True 
    

    return False
    
