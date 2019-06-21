import {PrincipleHeader} from './PrincipleHeader';

export class Principle {
    private _id: number;
    private _definition: string;
    private _principleHeaderID: number;
    

    constructor(id: number, definition: string) {
        this._id = id;
        this._definition = definition;
        
    }

    get id(): number {
        return this._id;
    }

    set id(value: number) {
        this._id = value;
    }

    get definition(): string {
        return this._definition;
    }

    set definition(value: string) {
        this._definition = value;
    }
    
    
    get principleHeaderID(): number {
        return this._principleHeaderID;
    }
    
    set principleHeaderID(value: number) {
        this._principleHeaderID = value;
    }
}
