import requests
from getcredentials import geturl, gettkn


def get_project():
    url = f"{geturl()}/api/projects/search"
    auth = (gettkn(), "")
    response = requests.get(url, auth=auth, timeout=10)

    if response.status_code == 200:
        projects = response.json()["components"]
        for project in projects:
            print(project["key"])
    else:
        print("Error al hacer la solicitud HTTP")


get_project()
