import { GeocodeEntity } from "../../entities/geocode.entity";
import { GeocodeService } from "../../../presentation/geocode/geocode.service";

import { PrismaClient } from '@prisma/client';
import { PronosticoService } from '../../../presentation/geocode/pronostico.service';
import e from "express";


interface FillPronosticosDatabaseUseCase {
    execute: (cities: string[]) => Promise<boolean>
}

export class FillPronosticosDatabase implements FillPronosticosDatabaseUseCase {

    constructor(
        private readonly geocodeService: GeocodeService,
        private readonly pronosticoService: PronosticoService

    ){}

    async execute(cities: string[]): Promise<boolean> {
        const prisma = new PrismaClient();
        try {
            for (const city of cities) {
                console.log('Processing city:', city);
                const data = await this.geocodeService.getCityFromDatabase(city);
                if (data instanceof GeocodeEntity) {
                   const pronosticos = await this.pronosticoService.getWeather5days(data);
                   const cleanedData = this.pronosticoService.cleanWeatherData(pronosticos);

                     for (const pronostico of cleanedData) {
                        const weather = await prisma.condicionMeteorologica.findFirst({
                            where: {
                                id: pronostico.weather.id
                            }
                        });
                        if (!weather) {
                            await prisma.condicionMeteorologica.create({
                                data: {
                                    id: pronostico.weather.id,
                                    tipo: pronostico.weather.main,
                                    detalle: pronostico.weather.description
                                }
                            });
                        }
                       const cityId = await prisma.ciudad.findFirst({
                           where: {
                               nombre: city
                           },
                           select: {
                               id: true
                           }
                       }); 
                       if(!cityId || cityId.id === undefined) {
                         throw new Error(`City ${city} not found in database`);
                        }
                        const pronosticoExist = await prisma.prevision.findFirst({
                            where: {
                                ciudadId: cityId.id,
                                fecha: pronostico.date,
                            }
                        });
                        if (pronosticoExist) {
        
                        } else {
                            try {
                                 await prisma.prevision.create({
                                data: {
                                    ciudadId: cityId.id,
                                    fecha: pronostico.date,
                                    temperaturaMaxima: pronostico.maxTemperature,
                                    temperaturaMinima: pronostico.minTemperature,
                                    condicionId : pronostico.weather.id
                                }
                            });
                            } catch (error) {
                                console.error(`Error creating forecast for city ${city}:`, error);
                                throw new Error(`Error creating forecast for city ${city}`);
                                
                            }
                           
                        }
                    }
                }
            }

            return true;
        } catch (error) {
            return false;
        }
    }

}