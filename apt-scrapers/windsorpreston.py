import requests

def windsorpreston():
  endpoint = "https://sightmap.com/app/api/v1/y8pxknjqv19/sightmaps/81021"
  
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
  }

  try:
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()["data"]
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Windsor Preston API: {e}")
    return []

if __name__ == "__main__":
  data = windsorpreston()
  print(f"Retrieved {len(data['units'])} records from Windsor Preston")