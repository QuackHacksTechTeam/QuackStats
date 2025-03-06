
from github import Github
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Exclusions for lines of code contributions 
# So LOC code is not effected by build files, binaries, etc. 
LINE_THRESHOLD = 1000 
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
    


def lines_of_code_by_user(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containng usernames and the total lines of 
    code they have contributed to the repo 

    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    contributers = repo.get_contributors()
    
    user_line_counts = {}

    for contributer in contributers: 
        commits = repo.get_commits(author=contributer)
        total_lines = 0

        for commit in commits: 
            for file in commit.files: 
                if is_excluded_file(file): 
                    continue
                total_lines += file.additions - file.deletions
        user_line_counts[contributer.login] = total_lines

    return user_line_counts



def commit_history_by_repo(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containing the repo name and
    the total number of commits from  the repo 

    """
    g = Github(GITHUB_TOKEN) 
    repo = g.get_repo(f"{owner}/{repo_name}")

    commits = repo.get_commits().totalCount
    return { repo_name: commits }


def commit_history_by_user(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containing the number of commits 
    each user has made from a repo

    {
        user: commit_num, 
        user: commit_num, 
        ...
    }
    """

    user_commits = {}

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    commits = repo.get_commits() 
    for commit in commits: 
        if commit.author is None: 
            continue

        user = commit.author.login

        if user in user_commits: 
            user_commits[user] += 1
        else: 
            user_commits[user] = 1

    return user_commits




