class SnowData:

    def __init__(
        self,
        resort_name,
        previous_night,
        last_24_hours,
        last_72_hours,
        daily_snowfall
    ):
        self.resort_name = resort_name
        self.previous_night = previous_night
        self.last_24_hours = last_24_hours
        self.last_72_hours = last_72_hours
        self.daily_snowfall = daily_snowfall

    def to_dict(self):
        return {
            "resort": self.resort_name,
            "previous_night_cm": self.previous_night,
            "last_24_hours_cm": self.last_24_hours,
            "last_72_hours_cm": self.last_72_hours,
            "daily_snowfall_cm": self.daily_snowfall
        }
