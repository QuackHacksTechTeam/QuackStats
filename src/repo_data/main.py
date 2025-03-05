
import gh_requests 

def main(): 

    commit_history = gh_requests.get_commit_history("QuackHacksTechTeam", "GitRank")

    if (commit_history is None): 
        print("Invalid request")
        return 
        
    commits = gh_requests.get_user_commits(commit_history)
    commit_ranking = { user: commits.count(user) for user in set(commits) }

    print(commit_ranking)


if __name__ == "__main__": 
    main()















    



