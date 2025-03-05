

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


#---------------------------------------------------
load_dotenv()
FRONTEND_PATH = "../frontend/build"
app = Flask(__name__, static_folder=FRONTEND_PATH + '/static', static_url_path='/static')

PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "localhost")

REPO_TEXT_FILE = "../repos.txt"
REPO_URLS = repo_url_reader.read_urls(REPO_TEXT_FILE)
# ---------------------------------------------------


@app.route('/')
def serve_react_app():
    return send_from_directory(os.path.join(app.root_path, FRONTEND_PATH), 'index.html')


# ----------------------- API --------------------------

@app.route('/user-commits', methods=['GET'])
def get_user_commits(): 
    """
    Send all user commit history in json 

    """

    all_user_commits = {}
    for repo_url in REPO_URLS: 
        if not repo_url: 
            continue

        # Parse the url 
        parsed_url = repo_url_reader.get_owner_reponame(repo_url) 
        if parsed_url is None: 
            print(f"Error parsing repo url: {repo_url}")
            continue
        owner, reponame = parsed_url

        # Try to append all users commits to the overall dict 
        try: 
            users_commit_history = gh_requests.commit_history_by_user(owner, reponame)
            for user, num_commits in users_commit_history.items(): 
                if user not in all_user_commits: 
                    all_user_commits[user] = num_commits
                else: 
                    all_user_commits[user] += num_commits

        except Exception:  
            return jsonify({ "Error": "Invalid GitHub API request" })

    all_user_commit_list = [{"username": user, "commits": count} for user, count in all_user_commits.items()]
    return jsonify(all_user_commit_list)


if __name__ == "__main__": 
    app.run(host=HOST, port=PORT, debug=True)















    



