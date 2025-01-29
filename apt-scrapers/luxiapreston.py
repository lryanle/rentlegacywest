import requests

def luxiapreston():
  endpoint = "https://sightmap.com/app/api/v1/8ywkd39gplx/sightmaps/85901"
  
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
  }

  try:
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()["data"]
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Luxia Preston API: {e}")
    return []

if __name__ == "__main__":
  data = luxiapreston()
  print(f"Retrieved {len(data['units'])} records from Luxia Preston")