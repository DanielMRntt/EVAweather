import { Request, Response } from "express";
import { PrevisionService } from "../services/prevision.service";
import { evaEntity } from '../../domain/entities/evaEntity,entity';



export class PrevisionController {
    constructor (
        private readonly previsionService: PrevisionService,
    ){}

    webhookHandler = async (req: Request, res: Response) => {
        const { entities } = req.body;
        
        const evaEntities: evaEntity[] = entities.map(evaEntity.fromObject);

        const date =  evaEntities
        .filter(entity => entity.name === "DATE")
        .map(entity => entity.value).pop();

        const cities = evaEntities
        .filter(entity => entity.name === "Ciudad")
        .map(entity => entity.value);
      
        const [day, month, year] = date!.split("/");
        const formatedDate = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));

        const previsiones = await Promise.all(
            cities.map(async (city) => {
                return await this.previsionService.obtenerPrevision(city, formatedDate);
            })
        ); 
        if (previsiones === null || previsiones.length === 0) {
                    res.status(400).json({  "option": "NORESULT", "openContext": {},"visibleContext": {},"hiddenContext": {}})
                }

        const response = this.previsionService.returnResponse(previsiones);
        res.status(200).json(response);
    }
}