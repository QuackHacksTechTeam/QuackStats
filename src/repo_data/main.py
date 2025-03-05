

import requests 

from dotenv import load_dotenv
import os

load_dotenv()

OWNER = "QuackHacksTechTeam"
REPO = "GitRank"
GITHUB_API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
TOKEN = os.getenv("GITHUB_TOKEN")


def get_user_commits(owner: str, repo: str): 

    headers = { 
               "Accept": "application/vnd.github+json",
               "Authorization": f"Bearer {TOKEN}",
               "X-Github-API-Version": "2022-11-28"
              }

    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code != 200: 
        return None

    users = []
    for commit in response.json(): 
        users.append(commit["committer"]["login"])

    return users; 


def main(): 

    commits = get_user_commits(OWNER, REPO)
    print(commits)



if __name__ == "__main__": 
    main()















    



