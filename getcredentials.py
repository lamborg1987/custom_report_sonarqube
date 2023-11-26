"""set and get url auth starttime"""
from datetime import datetime

# set


def seturl(url):
    """Set url base sonarquebe ejem: http://sonarqube:9000 o https://sonarquebe"""
    with open("report.cache", "w", encoding="utf-8") as f:
        f.write(f"url:{url}")


def settkn(tkn):
    """Set user or token for authentication sonarqube"""
    with open("report.cache", "a", encoding="utf-8") as f:
        f.write(f"\ntkn:{tkn}")


def setstm():
    """Set date time start program"""
    starttime = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    with open("report.cache", "a", encoding="utf-8") as f:
        f.write(f"\nstm:{starttime}")


# get


def geturl():
    """Get url base sonarqube"""
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "url":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


def gettkn():
    """Get user or token sonarqube"""
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "tkn":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


def getstm():
    """Get start time"""
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "stm":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea
        return None


# seturl("http://scm.cloudconsisint.com:9000")
# settkn("squ_e17f7795ecd4091d57a52690cf4ea5a138087b7e")
# setstm()
# getstm()
