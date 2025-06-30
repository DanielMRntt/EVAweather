
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Ciudad(Base):
    __tablename__ = 'ciudad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)

    previsiones = relationship("Prevision", back_populates="ciudad")

class CondicionMeteorologica(Base):
    __tablename__ = 'condicion_meteorologica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    detalle = Column(String, nullable=False)

    previsiones = relationship("Prevision", back_populates="condicion")

class Prevision(Base):
    __tablename__ = 'prevision'
    __table_args__ = (UniqueConstraint('ciudadId', 'fecha', name='uix_ciudad_fecha'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    temperaturaMinima = Column(Float, nullable=False)
    temperaturaMaxima = Column(Float, nullable=False)

    ciudadId = Column(Integer, ForeignKey('ciudad.id'), nullable=False)
    condicionId = Column(Integer, ForeignKey('condicion_meteorologica.id'), nullable=False)

    ciudad = relationship("Ciudad", back_populates="previsiones")
    condicion = relationship("CondicionMeteorologica", back_populates="previsiones")
