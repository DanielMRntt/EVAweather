from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos
DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5434/Weather"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
