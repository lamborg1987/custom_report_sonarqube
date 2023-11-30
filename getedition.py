"""find and validate sonarqube edition"""
import requests
from getcredentials import geturl, gettkn


def get_sonar_edition():
    """Get edition"""
    url = f"{geturl()}/api/navigation/global"
    auth = (gettkn(), "")
    try:
        response = requests.get(url, auth=auth, timeout=10)
        response.raise_for_status()
        edition = response.json()["edition"]
        return edition
    except requests.exceptions.RequestException as e:
        print(f"Error de comunicación: {e}")
    return None


def validate_nocommunity():
    """Validate edition diferent community"""
    edition = get_sonar_edition()
    if edition == "Community" or edition is None:
        return False
    return True
