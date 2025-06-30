# app/use_cases/fill_cities_database.py

from app.domain.geocode_entity import GeocodeEntity
from app.servicios.geocodeService import GeocodeService
from app.modelos.modelos import Ciudad
from app.modelos.session import SessionLocal

class FillCitiesDatabase:
    def __init__(self, geocode_service: GeocodeService):
        self.geocode_service = geocode_service

    def execute(self, cities: list[str]) -> bool:
        session = SessionLocal()
        try:
            for city in cities:
                data = self.geocode_service.geocode_from_api(city)
                if isinstance(data, GeocodeEntity):
                    existing_city = session.query(Ciudad).filter_by(nombre=data.city).first()
                    if existing_city:
                        continue
                    new_city = Ciudad(
                        nombre=data.city,
                        latitud=data.latitude,
                        longitud=data.longitude
                    )
                    session.add(new_city)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False
        finally:
            session.close()
