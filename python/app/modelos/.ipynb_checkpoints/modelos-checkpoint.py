{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6271ea67-9a89-46e0-a647-31d061cf0c67",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, create_engine\n",
    "from sqlalchemy.orm import relationship, declarative_base\n",
    "\n",
    "# Definir la base para los modelos\n",
    "Base = declarative_base()\n",
    "\n",
    "# Modelo Ciudad\n",
    "class Ciudad(Base):\n",
    "    __tablename__ = 'ciudad'\n",
    "\n",
    "    id = Column(Integer, primary_key=True, autoincrement=True)\n",
    "    nombre = Column(String, nullable=False)\n",
    "    latitud = Column(Float, nullable=False)\n",
    "    longitud = Column(Float, nullable=False)\n",
    "\n",
    "    previsiones = relationship(\"Prevision\", back_populates=\"ciudad\")\n",
    "\n",
    "# Modelo CondicionMeteorologica\n",
    "class CondicionMeteorologica(Base):\n",
    "    __tablename__ = 'condicion_meteorologica'\n",
    "\n",
    "    id = Column(Integer, primary_key=True, autoincrement=True)\n",
    "    tipo = Column(String, nullable=False)\n",
    "    detalle = Column(String, nullable=False)\n",
    "\n",
    "    previsiones = relationship(\"Prevision\", back_populates=\"condicion\")\n",
    "\n",
    "# Modelo Prevision\n",
    "class Prevision(Base):\n",
    "    __tablename__ = 'prevision'\n",
    "    __table_args__ = (UniqueConstraint('ciudadId', 'fecha', name='uix_ciudad_fecha'),)\n",
    "\n",
    "    id = Column(Integer, primary_key=True, autoincrement=True)\n",
    "    fecha = Column(DateTime, nullable=False)\n",
    "    temperaturaMinima = Column(Float, nullable=False)\n",
    "    temperaturaMaxima = Column(Float, nullable=False)\n",
    "\n",
    "    ciudadId = Column(Integer, ForeignKey('ciudad.id'), nullable=False)\n",
    "    condicionId = Column(Integer, ForeignKey('condicion_meteorologica.id'), nullable=False)\n",
    "\n",
    "    ciudad = relationship(\"Ciudad\", back_populates=\"previsiones\")\n",
    "    condicion = relationship(\"CondicionMeteorologica\", back_populates=\"previsiones\")\n",
    "\n",
    "# Crear las tablas si no existen\n",
    "if __name__ == \"__main__\":\n",
    "    # Reemplaza con tus credenciales reales\n",
    "    engine = create_engine(\"postgresql+psycopg2://usuario:contraseña@localhost:5432/tu_bbdd\")\n",
    "    Base.metadata.create_all(engine)\n",
    "    print(\"Tablas creadas si no existían previamente.\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
