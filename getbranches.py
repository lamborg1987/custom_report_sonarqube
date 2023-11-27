"""Get branches in project"""
import requests
from getcredentials import geturl, gettkn


def get_branches(projecto):
    """Get branches in project"""
    url = f"{geturl()}/api/project_branches/list"
    auth = (gettkn(), "")
    abranch = []
    querystring = {"project": projecto}
    response = requests.get(url, params=querystring, auth=auth, timeout=10)

    if response.status_code == 200:
        branches = response.json()["branches"]
        for branch in branches:
            abranch += [branch["name"]]
            return abranch
    else:
        print("Error al hacer la solicitud HTTP")
        return False
