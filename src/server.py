

"""
REST API for github repo data
Essentially just a wrapper around the github api, to be used with a data displaying 
frontend

"""

from flask import Flask, jsonify, send_from_directory
import os
from dotenv import load_dotenv

import gh_requests 
import repo_url_reader
from response_types import RepoCommits


#---------------------------------------------------
load_dotenv()
FRONTEND_PATH = "../frontend/build"
app = Flask(__name__, static_folder=FRONTEND_PATH + '/static', static_url_path='/static')

PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "localhost")

REPO_TEXT_FILE = "repos.txt"
REPO_URLS = repo_url_reader.read_urls(REPO_TEXT_FILE)
# ---------------------------------------------------


@app.route('/')
def serve_react_app():
    return send_from_directory(os.path.join(app.root_path, FRONTEND_PATH), 'index.html')


# ----------------------- API --------------------------

@app.route('/commits', methods=['GET'])
def get_commit_data(): 
    """
    Send all commit history in json 
    Sends all in one response to limit the api requests to github 

    """

    all_repo_commits: list[RepoCommits] = []
    for repo_url in REPO_URLS: 
        owner, reponame = repo_url_reader.get_owner_reponame(repo_url)

        commit_history = gh_requests.get_commit_history(owner, reponame)
        if (commit_history is None): 
            return jsonify({ "Error": "Invalid GitHub API request" })

        user_commits = gh_requests.get_user_commits(commit_history)
        user_commit_ranking = { user: user_commits.count(user) for user in set(user_commits) }

        repo = RepoCommits(owner=owner, name=reponame, user_commits=user_commit_ranking)
        all_repo_commits.append(repo)

    return jsonify(all_repo_commits)



if __name__ == "__main__": 
    app.run(host=HOST, port=PORT, debug=True)















    



