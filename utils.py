def format_docker_url(docker_url: str) -> str:
    url_parts = docker_url.replace("https://hub.docker.com/", "").split('/')

    if url_parts[0] == '_':
        if len(url_parts) > 1:
            return url_parts[1]
        else:
            raise ValueError("Invalid Docker Hub URL format")
        
    elif url_parts[0] == 'r':
        if len(url_parts) > 2:
            user_name = url_parts[1]
            repo_name = url_parts[2]
            return f"{user_name}/{repo_name}"
        else:
            raise ValueError("Invalid Docker Hub URL format")
    
    else:
        raise ValueError("Invalid Docker Hub URL format")