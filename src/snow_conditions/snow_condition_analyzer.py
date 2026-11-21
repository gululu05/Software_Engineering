
class SnowConditionAnalyzer:

    RATINGS = [
        (20, "Excellent"),
        (10, "Good"),
        (3, "Moderate"),
        (0, "Poor")
    ]

    def evaluate(self, snow_data):
        snowfall = snow_data.last_24_hours

        if snowfall is None:
            return {
                "rating": "Unknown",
                "snowfall_cm": None,
                "description": "Insufficient snowfall data."
            }

        rating = "Poor"

        for threshold, name in self.RATINGS:
            if snowfall >= threshold:
                rating = name
                break

        return {
            "rating": rating,
            "snowfall_cm": snowfall,
            "snowfall_72h_cm": snow_data.last_72_hours,
            "previous_night_cm": snow_data.previous_night
        }
