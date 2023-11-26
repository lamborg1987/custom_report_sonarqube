from datetime import datetime


def seturl(url):
    with open("report.cache", "w", encoding="utf-8") as f:
        f.write(f"url:{url}")


def geturl():
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "url":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea


def settkn(tkn):
    with open("report.cache", "a", encoding="utf-8") as f:
        f.write(f"\ntkn:{tkn}")


def gettkn():
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "tkn":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea


def setstm():
    starttime = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    with open("report.cache", "a", encoding="utf-8") as f:
        f.write(f"\nstm:{starttime}")


def getstm():
    with open("report.cache", encoding="utf-8") as f:
        for line in f:
            if line[:3] == "stm":
                linea = line[4:]
                linea = linea.rstrip()
                # print(linea)
                return linea


seturl("http://scm.cloudconsisint.com:9000")
settkn("squ_e17f7795ecd4091d57a52690cf4ea5a138087b7e")
setstm()
getstm()
