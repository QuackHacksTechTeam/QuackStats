
import requests 

import os


GITHUB_API_REPO_URL = f"https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_commit_history(owner: str, repo: str): 
    """
    Sends an api request to get the json for the commit history of a repo. 
    To be parsed with various parser functions below 
    """
    headers = { 
               "Accept": "application/vnd.github+json",
               "Authorization": f"Bearer {GITHUB_TOKEN}",
               "X-Github-API-Version": "2022-11-28"
              }

    url = f"{GITHUB_API_REPO_URL}/{owner}/{repo}/commits"

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None 


def get_user_commits(commit_history) -> list[str]: 
    """
    Get all users that have commited to a repo from commit history json  
    User will repeat with each commit 

    """
    users = []
    for commit in commit_history: 
        if commit is None: 
            continue
        if "commit" not in commit: 
            continue
        if commit["commit"] is None:  # Ensure committer is not None
            continue

        user = commit["commit"]["author"]["name"]
        if user is None: 
            user = commit["committer"]["name"]

        if user != "web-flow":  # Avoid adding "web-flow"
            users.append(user)

    return users


