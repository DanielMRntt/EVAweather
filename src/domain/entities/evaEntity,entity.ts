export class evaEntity {
    constructor(
        public name: string,
        public value: string,
    ) {}

    public static fromObject(object: { [key: string]: any }): evaEntity {
        return new evaEntity(
            object.name,
            object.value
        );
    }
}
