import requests
from sqlalchemy.orm import Session
from app.modelos.modelos import Ciudad
from app.domain.geocode_entity import GeocodeEntity
from app.config.envs import WEATHER_API_GEO_URL, WEATHER_API_KEY


class GeocodeService:

    def geocode_from_api(self, city: str) -> GeocodeEntity | None:
        try:
            response = requests.get(
                WEATHER_API_GEO_URL,
                params={
                    "q": city,
                    "limit": 1,
                    "appid": WEATHER_API_KEY
                },
                verify=False  # ⚠️ Solo si estás seguro de desactivar SSL
            )
            response.raise_for_status()
            data = response.json()[0]
            return GeocodeEntity.from_dict({
                "city": city,
                "latitude": data["lat"],
                "longitude": data["lon"]
            })
        except Exception as e:
            print(f"Error al consultar la API: {e}")
            return None

    def get_city_from_database(self, session: Session, city: str) -> GeocodeEntity | None:
        try:
            ciudad = session.query(Ciudad).filter_by(nombre=city).first()
            if not ciudad:
                raise ValueError(f"City {city} not found in database")
            return GeocodeEntity.from_dict({
                "city": ciudad.nombre,
                "latitude": ciudad.latitud,
                "longitude": ciudad.longitud
            })
        except Exception as e:
            print(f"Error al consultar la base de datos: {e}")
            return None
