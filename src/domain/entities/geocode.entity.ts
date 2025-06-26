export class GeocodeEntity {
    constructor(
        public city: string,
        public latitude: number,
        public longitude: number,
    ){}

    public static fromObject(object: {[key: string] : any}) : GeocodeEntity {
        const { city, latitude, longitude } = object;
        return new GeocodeEntity(
            city,
            latitude,
            longitude
        );
    }
}