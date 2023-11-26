"""find and validate sonarqube edition"""
import requests
from getcredentials import geturl, gettkn


def get_sonar_edition():
    """Get edition"""
    url = f"{geturl()}/api/system/info"
    auth = (gettkn(), "")
    try:
        response = requests.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        edition = response.json()["System"]
        return edition["Edition"]
    except requests.exceptions.RequestException as e:
        print(f"Error de comunicación: {e}")
    return None


def validate_nocommunity():
    """Validate edition diferent community"""
    if get_sonar_edition() == "Community":
        return False
    return True


# print(get_sonar_edition())
# print(validate_nocommunity())
