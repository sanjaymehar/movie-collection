import requests


def get_data_from_credy():
    api_url = "https://demo.credy.in/api/v1/maya/movies/"
    response = requests.get(api_url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve movie data"}