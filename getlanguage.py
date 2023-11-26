"""Module get languages for x project"""
import requests
from getcredentials import geturl, gettkn


def check_language(projecto, lenguage):
    """check language exist in the project"""
    url = f"{geturl()}/api/issues/search"
    auth = (gettkn(), "")
    querystring = {"projects": projecto, "languages": lenguage, "ps": 1}
    try:
        response = requests.get(url, params=querystring, auth=auth, timeout=10)
        response.raise_for_status()
        if response.json()["total"] > 0:
            return lenguage
    except requests.exceptions.RequestException as e:
        print(f"Error de comunicación: {e}")
    return None


def get_languages(projecto):
    """check all posible language"""
    lenguagesactive = []
    lenguages = (
        "abap",
        "apex",
        "c",
        "cs",
        "cpp",
        "cobol",
        "css",
        "cloudformation",
        "docker",
        "flex",
        "go",
        "web",
        "json",
        "jsp",
        "java",
        "js",
        "kotlin",
        "kubernetes",
        "objc",
        "php",
        "pli",
        "plsql",
        "py",
        "rpg",
        "ruby",
        "scala",
        "secrets",
        "swift",
        "tsql",
        "terraform",
        "text",
        "ts",
        "vbnet",
        "vb",
        "xml",
        "yaml",
    )

    for lenguage in lenguages:
        if check_language(projecto, lenguage) is not None:
            lenguagesactive += [check_language(projecto, lenguage)]
    # print(lenguagesactive)
    return lenguagesactive


# get_languages("master-alfa")
# get_languages("RE-SECREX-20220531")
