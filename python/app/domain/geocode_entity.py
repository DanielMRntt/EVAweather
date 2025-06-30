class GeocodeEntity:
    def __init__(self, city: str, latitude: float, longitude: float):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_dict(data: dict) -> 'GeocodeEntity':
        return GeocodeEntity(
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
