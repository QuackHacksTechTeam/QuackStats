
from github import Github 
import os
from gh_requests.exclude_loc import is_excluded_file 
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def lines_of_code_by_repo(owner: str, repo_name: str) -> int: 
    """
    Returns the total lines of code from a repo 

    Does not include new lines 
    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    latest_commit = repo.get_branch(repo.default_branch).commit
    tree = repo.get_git_tree(latest_commit.sha, recursive=True)
    total_lines = 0

    for element in tree.tree:
        if element.type == "blob" and not is_excluded_file(element.path):
            blob = repo.get_git_blob(element.sha)
            content = base64.b64decode(blob.content).decode("utf-8", errors="ignore")
            non_empty_lines = [line for line in content.splitlines() if line.strip()]
            total_lines += len(non_empty_lines)
    return total_lines


def lines_of_code_by_user(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containng usernames and the total lines of 
    code they have contributed to the repo 


    IN PROGRESS 

    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    contributers = repo.get_contributors()
    
    user_line_counts = {}

    for contributer in contributers: 
        seen_files = set()
        total_lines = 0
        commits = repo.get_commits(author=contributer)

        for commit in commits:
            for file in commit.files:
                if file.status == "removed" or is_excluded_file(file.filename):
                    continue
                
                key = (file.filename, commit.sha)
                if key in seen_files:
                    continue
                
                seen_files.add(key)
                
                blob = repo.get_git_blob(file.sha)
                if blob.encoding == "base64":
                    content = base64.b64decode(blob.content).decode('utf-8', errors='ignore')
                    lines = [line for line in content.splitlines() if line.strip() != '']
                    total_lines += len(lines) - file.deletions

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




