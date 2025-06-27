
export interface WeatherData {
    id: number;
    main: string;
    description: string;
}

export class PronosticoEntity {
    constructor(
        public date: Date,
        public maxTemperature: number,
        public minTemperature: number,
        public weather: WeatherData,
    ){}

     public static fromObject(object: {[key: string] : any}) : PronosticoEntity {
    
        const { date, maxTemperature, minTemperature, weather } = object;
        return new PronosticoEntity(
            date,
           parseFloat(maxTemperature),
            parseFloat(minTemperature),
            weather
        );
    }
}