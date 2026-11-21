
import requests

from .weather_forecast import WeatherForecast


class WeatherAPI:

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Rain showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    def __init__(self, timeout=10):
        self.timeout = timeout

    def get_tomorrows_forecast(
        self,
        resort_name
    ):
        # Open-Meteo returns today at index 0 and tomorrow at index 1.
        location = self.get_coordinates(resort_name)

        if location is None:
            return None

        latitude = location["latitude"]
        longitude = location["longitude"]

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum,"
                "snowfall_sum,"
                "weather_code"
            ),
            "forecast_days": 2,
            "timezone": "auto"
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            daily = data.get("daily", {})
            dates = daily.get("time", [])

            if len(dates) < 2:
                raise ValueError("Tomorrow's forecast unavailable")

            def get_value(key):
                values = daily.get(key, [])
                return values[1] if len(values) > 1 else None

            weather_code = get_value("weather_code")

            condition = (
                self.WEATHER_CODES.get(weather_code, "Unknown")
                if weather_code is not None
                else "Unknown"
            )

            return WeatherForecast(
                resort_name=resort_name,
                date=dates[1],
                min_temperature=get_value("temperature_2m_min"),
                max_temperature=get_value("temperature_2m_max"),
                precipitation=get_value("precipitation_sum"),
                snowfall=get_value("snowfall_sum"),
                weather_code=weather_code,
                condition=condition
            )

        except (requests.RequestException, ValueError) as error:
            print(f"Weather API error: {error}")
            return None

    def get_coordinates(self, resort_name):
        params = {
            "name": resort_name,
            "count": 5,
            "language": "en"
        }

        try:
            response = requests.get(
                self.GEOCODING_URL,
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
                "name": location["name"],
                "country": location.get("country"),
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "timezone": location.get("timezone", "auto")
            }

        except (requests.RequestException, KeyError, ValueError) as error:
            print(f"Geocoding error: {error}")
            return None
