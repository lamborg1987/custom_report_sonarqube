import time
import getcredentials
import getprojects
import getedition
import getbranches
import getlanguage
import getissues

# import compressreports

## severity: "INFO", "MINOR","MAJOR","CRITICAL","BLOCKER"
## type: "BUG", "VULNERABILITY", "CODE_SMELL"

# lenguage= abap,apex, c,cs "c#", cpp "c++", cobol, css,cloudformation, docker,flex, go,
# web "html", json,jsp,java,js,kotlin,kubernetes,objc "Objective-C", php, pli "PL/I",
# plsql "PL/SQL,py "python",rpg,ruby, scala,secrets,swift,tsql,terraform,text,ts "typescript",
#  vbnet,vb,xml,yaml

print("Welcome to personalized report generator for sonarqube ")
print("It is recommended to use an admin account")
print("type exit at any time to exit this app\n")
getcredentials.setstm()
getcredentials.seturl(input("Sonarqube base url: "))
getcredentials.settkn(input("Sonarqube user token: "))


getcredentials.validate_url()
getcredentials.validate_token()

projects = getprojects.get_project()
while True:
    if projects is None:
        print("\n\033[91mPROJECTS NOT FOUND\033[0m\n")
        getcredentials.exit_salir()
    print("\nAvailable projects:")
    for project in projects:
        print(project)

    project = input("\nSelect a project: ")
    if project in projects:
        break
    if project == "exit":
        getcredentials.exit_salir()
    print("\n\033[91mPROJECT SELECTED IS NOT FOUND\033[0m\n")

print(f"\nProject seleted: {project}")

EDITION = getedition.validate_nocommunity()

if EDITION is True:
    while True:
        print(f"\nAvailable branches for project: {project}")
        branches = getbranches.get_branches(project)
        for branch in branches:
            print(branch)
        branch = input("\nSelect branch: ")
        if branch in branches:
            break
        if branch == "exit":
            getcredentials.exit_salir()
        print("\n\033[91mBRANCH SELECTED IS NOT FOUND\033[0m\n")
    print(f"\nBranch seleted: {branch}")

while True:
    languages = getlanguage.get_languages(project)
    print(f"\nAvailable languages for project: {project}")
    for language in languages:
        print(language)
    language_input = input(
        "\nSelect language perarated by comma |  Press Enter (all language by default): "
    )
    if language_input == "exit":
        getcredentials.exit_salir()
    if language_input:
        language = [lang.strip() for lang in language_input.split(",")]
    else:
        language = languages
    all_languages_found = True
    for lang in language:
        if lang in languages:
            print(lang)
        else:
            print(f"\n\033[91mLANGUAGE SELECTED {lang} IS NOT FOUND\033[0m\n")
            all_languages_found = False
    if all_languages_found:
        break

print(f"\nLanguage seleted: {language}")

while True:
    issue_types = ["BUG", "VULNERABILITY", "CODE_SMELL"]
    issue_type_input = input(
        "\nSelect issue type perarated by comma # BUG, VULNERABILITY, CODE_SMELL |  Press Enter (all language by default): "
    )
    if issue_type_input == "exit":
        getcredentials.exit_salir()
    if issue_type_input:
        issue_type = [issuet.strip().upper() for issuet in issue_type_input.split(",")]
    else:
        issue_type = ["BUG", "VULNERABILITY", "CODE_SMELL"]
    all_issue_type_found = True
    for issue_t in issue_type:
        if issue_t in issue_types:
            print(issue_t)
        else:
            print("\n\033[91mISSUE TYPES  SELECTED IS NOT FOUND\033[0m\n")
            all_issue_type_found = False
    if all_issue_type_found:
        break

print(f"\nIssue type seleted: {issue_type}")

print("\nSelected parameters:\n")
print(f"Project: {project}")
print(f"Branch: {branch}")
print(f"Language: {language}")
print(f"Issues Type: {issue_type}")
while True:
    parameters = input("Is it correct? Type 'yes' or 'no': ").lower()
    if parameters == "exit":
        getcredentials.exit_salir()
    if parameters in ["yes", "no"]:
        break
    else:
        print("Invalid input. Please type 'yes' or 'no'.")

if "BUG" in issue_type:
    print("\ngenerating Bug reports")
    getissues.call_find_issues(project, "BUG", "INFO", language, branch)
    getissues.call_find_issues(project, "BUG", "MINOR", language, branch)
    getissues.call_find_issues(project, "BUG", "MAJOR", language, branch)
    getissues.call_find_issues(project, "BUG", "CRITICAL", language, branch)
    getissues.call_find_issues(project, "BUG", "BLOCKER", language, branch)

if "VULNERABILITY" in issue_type:
    print("generating Vulnerability reports")
    getissues.call_find_issues(project, "VULNERABILITY", "INFO", language, branch)
    getissues.call_find_issues(project, "VULNERABILITY", "MINOR", language, branch)
    getissues.call_find_issues(project, "VULNERABILITY", "MAJOR", language, branch)
    getissues.call_find_issues(project, "VULNERABILITY", "CRITICAL", language, branch)
    getissues.call_find_issues(project, "VULNERABILITY", "BLOCKER", language, branch)

if "CODE_SMELL" in issue_type:
    print("generating Code Smell reports")
    getissues.call_find_issues(project, "CODE_SMELL", "INFO", language, branch)
    getissues.call_find_issues(project, "CODE_SMELL", "MINOR", language, branch)
    getissues.call_find_issues(project, "CODE_SMELL", "MAJOR", language, branch)
    getissues.call_find_issues(project, "CODE_SMELL", "CRITICAL", language, branch)
    getissues.call_find_issues(project, "CODE_SMELL", "BLOCKER", language, branch)

time.sleep(120)

print("\ngenerating Full reports")
getissues.join_files("BUG")
getissues.join_files("VULNERABILITY")
getissues.join_files("CODE_SMELL")

getissues.join_full_report()
# print("\nCompressing reports")
# compressreports.compress()
print("Clean an exit")
getcredentials.exit_salir()