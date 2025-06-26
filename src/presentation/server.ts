import express, { Router } from 'express';
import path from 'path';
import { FillCitiesDatabase } from '../domain/use-cases/geocode/fill-database-cities';
import { GeocodeService } from './geocode/geocode.service';


export interface Options {
    port: number;
    public_path?: string;
    routes: Router;
}

const geocodeService = new GeocodeService();
const cities = [ "Barcelona", "Roma", "Andorra la Vella", "París"];


export class Server {

    public app = express();
    private serverListener?: any;
    private readonly port: number;
    private readonly publicPath: string;
    private readonly routes: Router;

    constructor(options: Options){
        const {port, routes, public_path = 'public'} = options;
        this.publicPath = public_path;
        this.port = port;
        this.routes= routes;

    }

    async start() {

        //* MiddelWares
        this.app.use(express.json());
        this.app.use(express.urlencoded({extended: true}));

        //*Public folder
        this.app.use(express.static(this.publicPath));

        //routes
        this.app.use(this.routes);


        this.serverListener = this.app.listen(this.port, () => {
            console.log(`Server running on Port ${this.port}`);
            //llenar la base de datos con las ciudades
            new FillCitiesDatabase(geocodeService).execute(cities);
        })
    }

     public close() {
    this.serverListener?.close();
  }


}