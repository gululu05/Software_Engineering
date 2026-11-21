import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from location.geocoding_api import GeocodingAPI
from .snow_data import SnowData


class SnowfallAPI:

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, geocoding_api=None, timeout=10):
        self.geocoding_api = geocoding_api or GeocodingAPI()
        self.timeout = timeout

    def get_snowfall(self, resort_name):
        location = self.geocoding_api.get_coordinates(resort_name)

        if location is None:
            return None

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "hourly": "snowfall",
            "daily": "snowfall_sum",
            "past_hours": 72,
            "past_days": 3,
            "timezone": location["timezone"]
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            hourly = data.get("hourly", {})
            daily = data.get("daily", {})

            times = hourly.get("time", [])
            snowfall = hourly.get("snowfall", [])

            if not times or not snowfall:
                return None

            timezone = ZoneInfo(data["timezone"])
            now = datetime.now(timezone)

            previous_night_start = (
                now.replace(hour=18, minute=0, second=0, microsecond=0)
                - timedelta(days=1)
            )

            previous_night_end = now.replace(
                hour=8, minute=0, second=0, microsecond=0
            )

            last_24_hours_start = now - timedelta(hours=24)
            last_72_hours_start = now - timedelta(hours=72)

            previous_night = []
            last_24_hours = []
            last_72_hours = []

            for time, amount in zip(times, snowfall):
                if amount is None:
                    continue

                timestamp = datetime.fromisoformat(time).replace(tzinfo=timezone)

                if timestamp >= previous_night_start and timestamp < previous_night_end:
                    previous_night.append(amount)

                if timestamp >= last_24_hours_start and timestamp <= now:
                    last_24_hours.append(amount)

                if timestamp >= last_72_hours_start and timestamp <= now:
                    last_72_hours.append(amount)

            def calculate_total(values):
                return round(sum(values), 1) if values else None

            daily_snowfall = {
                date: amount
                for date, amount in zip(
                    daily.get("time", []),
                    daily.get("snowfall_sum", [])
                )
            }

            return SnowData(
                resort_name=resort_name,
                previous_night=calculate_total(previous_night),
                last_24_hours=calculate_total(last_24_hours),
                last_72_hours=calculate_total(last_72_hours),
                daily_snowfall=daily_snowfall
            )

        except (requests.RequestException, ValueError, KeyError) as error:
            print(f"Snowfall API error: {error}")
            return None
