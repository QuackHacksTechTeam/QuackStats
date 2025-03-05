
from github import Github
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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




