"""Get issues and create reports csv"""
# import time
# from datetime import datetime
import math
import threading
import os
import pandas
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import requests
from getcredentials import geturl, gettkn, getstm

## severity: "INFO", "MINOR","MAJOR","CRITICAL","BLOCKER"
## type: "BUG", "VULNERABILITY", "CODE_SMELL"

# lenguage= abap,apex, c,cs "c#", cpp "c++", cobol, css,cloudformation, docker,flex, go,
# web "html", json,jsp,java,js,kotlin,kubernetes,objc "Objective-C", php, pli "PL/I",
# plsql "PL/SQL,py "python",rpg,ruby, scala,secrets,swift,tsql,terraform,text,ts "typescript",
#  vbnet,vb,xml,yaml


def find_issues(projecto, tipo, severity, lenguaje="", branch=""):
    """find issues with parameters: project, type, severity, language,
    branch #branch only for no community version."""
    url = f"{geturl()}/api/issues/search"
    auth = (gettkn(), "")
    # current_datetime = getstm()
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
        print(f"Se creo ruta {dirpath}")
    else:
        print(f"La ruta {dirpath} ya existe")

    if response.status_code == 200:
        paginas = math.ceil(response.json()["total"] / 100)
        if paginas > 100:
            print(
                "WARNING: solo se mostraran los primeros 10000 resultados para la busqueda"
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
                f"{dirpath}/{tipo}_{severity}_{lenguaje}_{getstm()}.csv",
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
    # issues_thread.join()


def join_files(tipo):
    """Join report files for specific issues types"""
    current_datetime = getstm()
    path = f"./{tipo}/"

    # Crear una lista de objetos Dask DataFrame para cada archivo CSV
    df_list = [
        dd.read_csv(os.path.join(path, archivo), dtype={"author": "object"})
        for archivo in os.listdir(path)
        if archivo.startswith(f"{tipo}") and archivo.endswith(".csv")
    ]

    # Concatenar los DataFrames en uno solo
    df_unido = dd.concat(df_list, ignore_index=True)

    # Guardar el resultado en un solo archivo CSV usando Dask
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
    final_path = f"./full-report_{current_datetime}.csv"
    paths = []
    file_pattern = "Full"
    df_list = []
    if os.path.exists(path_bug[0]):
        print("el archivo existe")
        paths += path_bug
        print(paths)
    else:
        print(f"no existe {path_bug}")

    if os.path.exists(path_vuln[0]):
        print("el archivo existe")
        paths += path_vuln
        print(paths)
    else:
        print(f"no existe {path_vuln}")

    if os.path.exists(path_csmell[0]):
        print("el archivo existe")
        paths += path_csmell
        print(paths)
    else:
        print(f"no existe {path_csmell}")

    for path in paths:
        files = [
            file
            for file in os.listdir(path)
            if file.startswith(file_pattern) and file.endswith(".csv")
        ]
        df_list.extend([dd.read_csv(os.path.join(path, file)) for file in files])
    df_join = dd.concat(df_list, ignore_index=True)
    df_join.compute().to_csv(final_path, index=False)


# call_find_issues("master-alfa", "BUG", "INFO", "java")
# call_find_issues("master-alfa", "BUG", "MINOR", "java")
# call_find_issues("master-alfa", "BUG", "MAJOR", "java")
# call_find_issues("master-alfa", "BUG", "CRITICAL", "java")
# call_find_issues("master-alfa", "BUG", "BLOCKER", "java")

# call_find_issues("master-alfa", "VULNERABILITY", "INFO", "java")
# call_find_issues("master-alfa", "VULNERABILITY", "MINOR", "java")
# call_find_issues("master-alfa", "VULNERABILITY", "MAJOR", "java")
# call_find_issues("master-alfa", "VULNERABILITY", "CRITICAL", "java")
# call_find_issues("master-alfa", "VULNERABILITY", "BLOCKER", "java")


# call_find_issues("master-alfa", "CODE_SMELL", "INFO", "java")
# call_find_issues("master-alfa", "CODE_SMELL", "MINOR", "java")
# call_find_issues("master-alfa", "CODE_SMELL", "MAJOR", "java")
# call_find_issues("master-alfa", "CODE_SMELL", "CRITICAL", "java")
# call_find_issues("master-alfa", "CODE_SMELL", "BLOCKER", "java")

# time.sleep(120)
# join_files("BUG")
# join_files("VULNERABILITY")
# join_files("CODE_SMELL")

# join_full_report()
