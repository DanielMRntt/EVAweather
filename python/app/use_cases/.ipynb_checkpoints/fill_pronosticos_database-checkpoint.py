# app/use_cases/fill_pronosticos_database.py

from app.entities.geocode_entity import GeocodeEntity
from app.services.geocode_service import GeocodeService
from app.services.pronostico_service import PronosticoService
from app.db.models import Ciudad, CondicionMeteorologica, Prevision
from app.db.session import SessionLocal

class FillPronosticosDatabase:
    def __init__(self, geocode_service: GeocodeService, pronostico_service: PronosticoService):
        self.geocode_service = geocode_service
        self.pronostico_service = pronostico_service

    def execute(self, cities: list[str]) -> bool:
        session = SessionLocal()
        try:
            for city in cities:
                print(f"Processing city: {city}")
                data = self.geocode_service.get_city_from_database(city, session)
                if isinstance(data, GeocodeEntity):
                    pronosticos_raw = self.pronostico_service.get_weather_5days(data)
                    cleaned_data = self.pronostico_service.clean_weather_data(pronosticos_raw)

                    for pronostico in cleaned_data:
                        # Verificar si la condición meteorológica ya existe
                        weather = session.query(CondicionMeteorologica).filter_by(id=pronostico.weather.id).first()
                        if not weather:
                            weather = CondicionMeteorologica(
                                id=pronostico.weather.id,
                                tipo=pronostico.weather.main,
                                detalle=pronostico.weather.description
                            )
                            session.add(weather)

                        # Obtener ID de la ciudad
                        city_record = session.query(Ciudad).filter_by(nombre=city).first()
                        if not city_record:
                            raise ValueError(f"City {city} not found in database")

                        # Verificar si ya existe el pronóstico
                        existing_forecast = session.query(Prevision).filter_by(
                            ciudad_id=city_record.id,
                            fecha=pronostico.date
                        ).first()

                        if not existing_forecast:
                            new_forecast = Prevision(
                                ciudad_id=city_record.id,
                                fecha=pronostico.date,
                                temperatura_maxima=pronostico.max_temperature,
                                temperatura_minima=pronostico.min_temperature,
                                condicion_id=pronostico.weather.id
                            )
                            session.add(new_forecast)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return False
        finally:
            session.close()
