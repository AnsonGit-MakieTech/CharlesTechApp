import requests

lat1 = 12.376257300431687
lon1 = 123.63006700549158

lat2 = 12.375397979169215
lon2 = 123.63353241958295

def get_osrm_route(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {
        'overview': 'full',
        'geometries': 'geojson'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['routes'][0]['geometry']['coordinates']  # List of [lon, lat]
    else:
        print("❌ OSRM API Error:", response.status_code)
        return []

route = get_osrm_route(lat1, lon1, lat2, lon2)
print(route)


def get_osrm_eta(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {
        'overview': 'false'  # We don’t need full coordinates here
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        route = data['routes'][0]
        distance_km = route['distance'] / 1000
        duration_min = route['duration'] / 60
        return round(distance_km, 2), round(duration_min, 2)
    else:
        print("❌ API Error:", res.status_code)
        return None, None

# Example usage
distance, duration = get_osrm_eta(lat1, lon1, lat2, lon2)
print(f"📍 Distance: {distance} km | 🕐 Duration: {duration} mins")

