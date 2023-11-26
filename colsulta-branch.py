import requests
from getcredentials import geturl, gettkn


def consultar_branch(projecto):
    url = f"{geturl()}/api/project_branches/list"
    auth = (gettkn(), "")
    querystring = {"project": projecto}
    response = requests.get(url, params=querystring, auth=auth, timeout=10)

    if response.status_code == 200:
        branches = response.json()["branches"]
        for branch in branches:
            print(branch["name"])
    else:
        print("Error al hacer la solicitud HTTP")


consultar_branch("master-alfa")
