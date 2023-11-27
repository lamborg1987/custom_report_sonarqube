"""Get issues and create reports csv"""
import math
import threading
import os
import pandas
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import requests
from getcredentials import geturl, gettkn, getstm


def find_issues(projecto, tipo, severity, lenguaje="", branch=""):
    """find issues with parameters: project, type, severity, language,
    branch #branch only for no community version."""
    url = f"{geturl()}/api/issues/search"
    auth = (gettkn(), "")
    dirpath = f"./{tipo}"
    if branch == "":
        querystring = {
            "projects": projecto,
            "types": tipo,
            "severities": severity,
            "languages": lenguaje,
            "p": 1,
        }
    else:
        querystring = {
            "projects": projecto,
            "types": tipo,
            "severities": severity,
            "languages": lenguaje,
            "p": 1,
            "branch": branch,
        }

    response = requests.get(url, params=querystring, auth=auth, timeout=10)

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    else:
        pass
    if response.status_code == 200:
        paginas = math.ceil(response.json()["total"] / 100)
        if paginas > 100:
            print(
                f"\033[93mWARNING: Only the first 10,000 results will be shown for the search. Type: {tipo} Severity: {severity}\033[0m"
            )
            paginas = 100
        while querystring["p"] <= paginas:
            issues = response.json()["issues"]

            if querystring["p"] == 1:
                df = pandas.DataFrame(
                    columns=[
                        "key",
                        "rule",
                        "severity",
                        "component",
                        "project",
                        "status",
                        "author",
                        "type",
                        "scope",
                    ]
                )
            for issue in issues:
                registro = {
                    "key": issue["key"],
                    "rule": issue["rule"],
                    "severity": issue["severity"],
                    "component": issue["component"],
                    "project": issue["project"],
                    "status": issue["status"],
                    "author": issue["author"],
                    "type": issue["type"],
                    "scope": issue["scope"],
                }
                df.loc[len(df)] = registro
            df.to_csv(
                f"{dirpath}/{tipo}_{severity}_{getstm()}.csv",
                index=False,
            )
            querystring["p"] += 1
            response = requests.get(url, params=querystring, auth=auth, timeout=10)
    else:
        print("Error al hacer la solicitud HTTP")


def call_find_issues(projecto, tipo, severity, lenguaje="", branch=""):
    """call find_issues in multi Thread"""
    issues_thread = threading.Thread(
        target=find_issues, args=(projecto, tipo, severity, lenguaje, branch)
    )
    issues_thread.start()


def join_files(tipo):
    """Join report files for specific issues types"""
    current_datetime = getstm()
    path = f"./{tipo}/"

    df_list = [
        dd.read_csv(os.path.join(path, archivo), dtype={"author": "object"})
        for archivo in os.listdir(path)
        if archivo.startswith(f"{tipo}") and archivo.endswith(".csv")
    ]

    df_unido = dd.concat(df_list, ignore_index=True)

    with ProgressBar():
        df_unido.compute().to_csv(
            f"{path}Full_{tipo}_{current_datetime}.csv", index=False
        )


def join_full_report():
    """Join all report files"""
    current_datetime = getstm()
    path_bug = ["./BUG/"]
    path_vuln = ["./VULNERABILITY/"]
    path_csmell = ["./CODE_SMELL/"]
    final_path = f"./FULL-REPORT_{current_datetime}.csv"
    paths = []
    file_pattern = "Full"
    df_list = []
    if os.path.exists(path_bug[0]):
        paths += path_bug
    else:
        print(f"no existe {path_bug}")

    if os.path.exists(path_vuln[0]):
        paths += path_vuln
    else:
        print(f"no existe {path_vuln}")

    if os.path.exists(path_csmell[0]):
        paths += path_csmell
    else:
        print(f"no existe {path_csmell}")

    for path in paths:
        files = [
            file
            for file in os.listdir(path)
            if file.startswith(file_pattern) and file.endswith(".csv")
        ]
        df_list.extend(
            [
                dd.read_csv(os.path.join(path, file), dtype={"author": "object"})
                for file in files
            ]
        )
    df_join = dd.concat(df_list, ignore_index=True)
    df_join.compute().to_csv(final_path, index=False)
