"""find projects in server sonarqube"""
import requests
from getcredentials import geturl, gettkn


def get_project():
    """Get projects"""
    projects_list = []
    url = f"{geturl()}/api/projects/search"
    auth = (gettkn(), "")
    try:
        response = requests.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        projects = response.json()["components"]
        for project in projects:
            projects_list += [project["key"]]
        return projects_list
    except requests.exceptions.RequestException as e:
        print(f"Error de comunicación: {e}")
    return None
