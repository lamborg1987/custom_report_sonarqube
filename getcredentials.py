"""set and get url auth starttime"""
from datetime import datetime
import sys
import os
import requests

FILECACHE = "report.cache"


def exit_salir():
    """exit and remove cache"""
    os.remove(FILECACHE)
    sys.exit()


# set


def seturl(url):
    """Set url base sonarquebe ejem: http://sonarqube:9000 o https://sonarquebe"""
    with open(FILECACHE, "a", encoding="utf-8") as f:
        f.write(f"\nurl:{url}")


def settkn(tkn):
    """Set user or token for authentication sonarqube"""
    with open(FILECACHE, "a", encoding="utf-8") as f:
        f.write(f"\ntkn:{tkn}")


def setstm():
    """Set date time start program"""
    starttime = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    with open(FILECACHE, "a", encoding="utf-8") as f:
        f.write(f"\nstm:{starttime}")


# get


def geturl():
    """Get url base sonarqube"""
    with open(FILECACHE, encoding="utf-8") as f:
        for line in f:
            if line[:3] == "url":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


def gettkn():
    """Get user or token sonarqube"""
    with open(FILECACHE, encoding="utf-8") as f:
        for line in f:
            if line[:3] == "tkn":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


def getstm():
    """Get start time"""
    with open(FILECACHE, encoding="utf-8") as f:
        for line in f:
            if line[:3] == "stm":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


# validate


def validate_url():
    """validate url is available"""

    try:
        response = requests.head(geturl(), timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            return True
        return response.status_code
    except requests.ConnectionError as e:
        print(f"\033[91mUrl is not correct: {e}\033[0m")
        exit_salir()
        return False
    except requests.exceptions.InvalidSchema as e:
        print(f"\033[91mProtocol http or https is not correct: {e}\033[0m")
        exit_salir()
        return False
    except requests.exceptions.MissingSchema as e:
        print(f"\033[91mUrl schema is not correct: {e}\033[0m")
        exit_salir()
        return False
    except requests.exceptions.InvalidURL as e:
        print(f"\033[91mUrl schema is not correct: {e}\033[0m")
        exit_salir()
        return False


def validate_token():
    """validate de user token is correct"""
    url = f"{geturl()}/api/system/ping"
    auth = (gettkn(), "")
    try:
        response = requests.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        if response.status_code == 200 and response.text == "pong":
            return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"\033[91mToken is not correct: {e}\033[0m")
        exit_salir()
        return False
