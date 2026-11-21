import requests


class GeocodingAPI:

    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, timeout=10):
        self.timeout = timeout

    def get_coordinates(self, location_name):

        params = {
            "name": location_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])

            if not results:
                return None

            location = results[0]

            return {
                "name": location.get("name"),
                "country": location.get("country"),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "timezone": location.get("timezone")
            }

        except (requests.RequestException, ValueError) as error:
            print(f"Geocoding API error: {error}")
            return None