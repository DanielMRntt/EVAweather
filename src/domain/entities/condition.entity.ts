export class ConditionEntity {
    constructor(
        public id: number,
        public name: string,
        public description: string,
    ){}

    public static fromObject(object: {[key: string] : any}) : ConditionEntity {
        const { id, name, description } = object;
        return new ConditionEntity(
            id,
            name,
            description
        );
    }
}