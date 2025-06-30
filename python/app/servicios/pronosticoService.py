import requests
from datetime import datetime
from collections import defaultdict, Counter
from app.domain.pronostico_entity import PronosticoEntity, WeatherData
from app.domain.geocode_entity import GeocodeEntity

class PronosticoService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_weather_5days(self, geocode):
        try:
            response = requests.get(
                self.base_url,
                params={
                    'lat': geocode.latitude,
                    'lon': geocode.longitude,
                    'appid': self.api_key
                },
                verify=False  # Equivalent to rejectUnauthorized: false
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def clean_weather_data(self, data):
        
        pronosticos = []
        weather_data_by_date = defaultdict(list)

        for item in data.get('list', []):
            date_str = datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d')
            max_temp = float(item['main']['temp_max']) - 273.15
            min_temp = float(item['main']['temp_min']) - 273.15
            weather = WeatherData(
                id=item['weather'][0]['id'],
                main=item['weather'][0]['main'],
                description=item['weather'][0]['description']
            )
            weather_data_by_date[date_str].append({
                'max_temp': max_temp,
                'min_temp': min_temp,
                'weather': weather
            })


        for date, entries in weather_data_by_date.items():
            max_temp = max(e['max_temp'] for e in entries)
            min_temp = min(e['min_temp'] for e in entries)

            weather_counter = Counter(
                (e['weather'].id, e['weather'].main, e['weather'].description)
                for e in entries
            )
            most_common_weather_key = weather_counter.most_common(1)[0][0]
            most_common_weather = WeatherData(*most_common_weather_key)

            pronosticos.append(
                PronosticoEntity.from_dict({
                    'date': datetime.strptime(date, '%Y-%m-%d').date().isoformat(),
                    'max_temperature': f"{max_temp:.2f}",
                    'min_temperature': f"{min_temp:.2f}",
                    'weather': most_common_weather
                })
            )

        return pronosticos
