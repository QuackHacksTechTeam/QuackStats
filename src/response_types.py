
from dataclasses import dataclass

@dataclass
class RepoCommits:
    owner: str
    name: str
    user_commits: dict[str, int]
    

