import requests


"""

-----------------    This is the Alternative File To Fetch Ip Location     ---------------------

"""

def get_public_ip_address():
    try:
        # Use a public IP address service to fetch the public IP
        response = requests.get("https://api.ipify.org")
        return response.text
    except Exception as e:
        print("Error fetching public IP address:", e)
        return None

def get_location_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)
        data = response.json()
        location = {
            "ip": data["ip"],
            "country": data["country"],
            "region": data.get("region"),  # Some IPs might not have region data
            "city": data["city"],
            "postal": data.get("postal"),
            "coordinates": data["loc"].split(",")
        }
        return location
    except Exception as e:
        print("Error fetching location information:", e)
        return None

def get_Location() -> dict:
    ip_address = get_public_ip_address()
    return get_location_info(ip_address)

if __name__ == "__main__":
    ip_address = get_public_ip_address()
    print("Public IP Address:", ip_address)
    
    location_info = get_location_info(ip_address)
    if location_info:
        print("\nLocation Information:")
        print("Country:", location_info["country"])
        print("Region:", location_info["region"])
        print("City:", location_info["city"])
        print("Postal : ",location_info['postal'])
        print("Latitude:", location_info["coordinates"][0])
        print("Longitude:", location_info["coordinates"][1])

