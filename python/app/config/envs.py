from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# Acceder a las variables
WEATHER_API_GEO_URL = os.getenv("WEATHER_API_BASE_GEO_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
