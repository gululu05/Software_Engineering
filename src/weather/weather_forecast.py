
class WeatherForecast:

    def __init__(
        self,
        resort_name,
        date,
        min_temperature,
        max_temperature,
        precipitation,
        snowfall,
        weather_code,
        condition
    ):
        self.resort_name = resort_name
        self.date = date
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.precipitation = precipitation
        self.snowfall = snowfall
        self.weather_code = weather_code
        self.condition = condition

    def to_dict(self):

        return {
            "resort": self.resort_name,
            "date": self.date,
            "temperature": {
                "min": self.min_temperature,
                "max": self.max_temperature
            },
            "precipitation": self.precipitation,
            "snowfall": self.snowfall,
            "weather_code": self.weather_code,
            "condition": self.condition
        }
