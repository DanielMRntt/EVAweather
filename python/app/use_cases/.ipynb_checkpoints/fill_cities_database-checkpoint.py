{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8634b638-2f43-4da8-96f0-6b34389ba708",
   "metadata": {},
   "outputs": [],
   "source": [
    "# app/use_cases/fill_cities_database.py\n",
    "\n",
    "from app.domain.geocode_entity import GeocodeEntity\n",
    "from app.servicios.geocode_service import GeocodeService\n",
    "from app.modelos.models import Ciudad\n",
    "from app.modelos.session import SessionLocal\n",
    "\n",
    "class FillCitiesDatabase:\n",
    "    def __init__(self, geocode_service: GeocodeService):\n",
    "        self.geocode_service = geocode_service\n",
    "\n",
    "    def execute(self, cities: list[str]) -> bool:\n",
    "        session = SessionLocal()\n",
    "        try:\n",
    "            for city in cities:\n",
    "                data = self.geocode_service.geocode_from_api(city)\n",
    "                if isinstance(data, GeocodeEntity):\n",
    "                    existing_city = session.query(Ciudad).filter_by(nombre=data.city).first()\n",
    "                    if existing_city:\n",
    "                        continue\n",
    "                    new_city = Ciudad(\n",
    "                        nombre=data.city,\n",
    "                        latitud=data.latitude,\n",
    "                        longitud=data.longitude\n",
    "                    )\n",
    "                    session.add(new_city)\n",
    "            session.commit()\n",
    "            return True\n",
    "        except Exception as e:\n",
    "            session.rollback()\n",
    "            print(f\"Error: {e}\")\n",
    "            return False\n",
    "        finally:\n",
    "            session.close()\n"
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
