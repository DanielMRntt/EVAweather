from datetime import datetime

class WeatherData:
    def __init__(self, id: int, main: str, description: str):
        self.id = id
        self.main = main
        self.description = description

    @staticmethod
    def from_dict(data: dict) -> 'WeatherData':
        return WeatherData(
            id=data.get('id'),
            main=data.get('main'),
            description=data.get('description')
        )

    def __repr__(self):
        return f"WeatherData(id={self.id}, main='{self.main}', description='{self.description}')"


class PronosticoEntity:
    def __init__(self, date: datetime, max_temperature: float, min_temperature: float, weather: WeatherData):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.weather = weather
    
    @staticmethod
    def from_dict(data: dict) -> 'PronosticoEntity':
        weather_data = data.get('weather')
        if isinstance(weather_data, dict):
            weather = WeatherData.from_dict(weather_data)
        elif isinstance(weather_data, WeatherData):
            weather = weather_data
        else:
            raise ValueError("Invalid type for 'weather' field")

        return PronosticoEntity(
            date=datetime.fromisoformat(data.get('date')),
            max_temperature=float(data.get('max_temperature')),
            min_temperature=float(data.get('min_temperature')),
            weather=weather
        )


    def __repr__(self):
        return (f"PronosticoEntity(date={self.date}, max_temperature={self.max_temperature}, "
                f"min_temperature={self.min_temperature}, weather={self.weather})")

