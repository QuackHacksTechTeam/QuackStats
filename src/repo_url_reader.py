


def read_urls(file_name: str) -> list[str]: 
    """
    Returns a list of urls with each url on a new line in a file 
    """
    urls = []
    with open(file_name, 'r') as urls_file: 
        for url in urls_file: 
            urls.append(url.strip())
    return urls; 

def get_owner_reponame(url: str) -> tuple[str, str] | None: 
    parts = url.split('/')
    if parts and len(parts) == 5: 
        owner = parts[3]
        repo = parts[4]
        return (owner, repo)

    return None



