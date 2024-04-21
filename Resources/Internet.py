import ipapi
import requests

def location() -> dict:
    """
    Returns the Ip Location of the System
    """
    return ipapi.location()


def IsAvailable() -> bool|None:
    """
    Returns True if Internet Is Available , if Not then False
    If the internet is having any problem or deley then it Returns None
    """
    try:
        response = requests.get("http://www.github.com", timeout=7)
        response.raise_for_status()
        return True  # Internet connection is available
    except requests.ConnectionError:
        return False  # No internet connection available
    except requests.Timeout:
        return None  # Request timed out
    except requests.RequestException as e:
        print("An error occurred:", e)
        return False  # Other request exception, assuming no internet connection


if __name__ == '__main__':
   print("Run >>>>>>>>  main.py <<<<<<<< File")