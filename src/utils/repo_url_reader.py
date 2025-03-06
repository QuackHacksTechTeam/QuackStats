

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
    """
    Parses an url into owner and reponame
    Returns None if the url not in a valid format 

    """
    parts = url.split('/')
    if parts and len(parts) == 5: 
        owner = parts[3]
        repo = parts[4]
        return (owner, repo)

    return None

def parse_urls(urls: list[str]) -> list[tuple[str, str]]: 
    """
    Parses all urls in a list into a list of tuples
    The tuples are (owner, reponame)

    """
    parsed = []
    for url in urls: 
        parsed_url = get_owner_reponame(url) 
        if parsed_url is None: 
            print(f"Error parsing repo url: {url}")
            continue
        parsed.append(parsed_url)
    return parsed



