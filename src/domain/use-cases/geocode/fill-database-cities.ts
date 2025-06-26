import { GeocodeEntity } from "../../entities/geocode.entity";
import { GeocodeService } from "../../../presentation/geocode/geocode.service";

import { PrismaClient } from '@prisma/client';






interface FillCitiesDatabaseUseCase {
    execute: (cities: string[]) => Promise<boolean>
}

export class FillCitiesDatabase implements FillCitiesDatabaseUseCase {

    constructor(
        private readonly geocodeService: GeocodeService,

    ){}

    async execute(cities: string[]): Promise<boolean> {
        const prisma = new PrismaClient();
        try {
            for (const city of cities) {
                const data = await this.geocodeService.geocodeFromApi(city);
                if (data instanceof GeocodeEntity) {
                    const existingCity = await prisma.ciudad.findFirst({
                        where: {
                            nombre: data.city
                        }
                    });
                    if (existingCity) {
                        continue;
                    }
                    await prisma.ciudad.create({
                        data: {
                            nombre: data.city,
                            latitud: data.latitude,
                            longitud: data.longitude
                        }
                    });
                } else {
                    throw new Error(`Failed to geocode city: ${city}`);
                }
            }

            return true;
        } catch (error) {
            return false;
        }
    };

}