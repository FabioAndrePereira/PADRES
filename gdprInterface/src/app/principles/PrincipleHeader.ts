export class  PrincipleHeader {
    private _id: number;
    private _type: string;
    
    constructor(id: number, type: string) {
        this._id = id;
        this._type = type;
    }

    get id(): number {
        return this._id;
    }
    
    set id(value: number) {
        this._id = value;
    }
    
    get type(): string {
        return this._type;
    }
    
    set type(value: string) {
        this._type = value;
    }
}
