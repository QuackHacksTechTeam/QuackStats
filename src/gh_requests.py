
import requests 

import os


GITHUB_API_REPO_URL = f"https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = { 
           "Accept": "application/vnd.github+json",
           "Authorization": f"Bearer {GITHUB_TOKEN}",
           "X-Github-API-Version": "2022-11-28"
          }


def get_branches(owner: str, repo: str) -> list[str]: 
    """
    Returns all of the branches of a repo 

    """
    url = f"{GITHUB_API_REPO_URL}/{owner}/{repo}/branches" 
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200: 
        print(f"Error fetching branches: {response.json()}")
        return []

    return [branch["name"] for branch in response.json()]


def filter_unique_commits(commit_history): 
    """
    Filter duplicate commits based on their SHA 

    """
    commits = []
    unique_commit_shas = set()

    for commit in commit_history: 
        if commit is None: 
            continue

        sha = commit["sha"]
        if sha in unique_commit_shas: 
            print("Duplicate found")
            continue

        unique_commit_shas.add(sha)
        commits.append(commit)

    return commits 

    

def get_commit_history(owner: str, repo: str): 
    """
    Sends an api request to get the json for the commit history of a repo. 
    To be parsed with various parser functions below 

    Searches through all branches and commit pages of the repo, 
    returning only unqiue commits 

    """

    commit_history = []

    branches = get_branches(owner, repo)
    for branch in branches: 

        url = f"{GITHUB_API_REPO_URL}/{owner}/{repo}/commits"

        # Search through all available pages
        page = 1
        while True: 
            print(f"Searching branch {branch} on page {page}")
            params = { "per_page": 100, "page": page, "sha": branch}
            response = requests.get(url, headers=HEADERS, params=params)

            if (response.status_code != 200): 
                print(f"Error: {response.status_code}, {response.json()}")
                return None

            commit_data = response.json()
            if not commit_data: 
                break 
            
            commit_history.extend(commit_data)
            page += 1


    return filter_unique_commits(commit_history)


def get_user_commits(commit_history) -> list[str]: 
    """
    Get all users that have commited to a repo from commit history json  
    User will repeat with each commit 

    """

    users = []

    for commit in commit_history: 
        if commit is None: 
            continue

        author = commit["author"]
        if author is None: 
            continue

        user = author["login"]

        if user is not None and user != "web-flow": 
            users.append(user)

    return users


