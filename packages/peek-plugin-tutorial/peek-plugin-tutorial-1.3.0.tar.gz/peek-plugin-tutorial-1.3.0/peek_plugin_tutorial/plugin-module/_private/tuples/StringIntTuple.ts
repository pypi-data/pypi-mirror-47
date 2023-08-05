import {addTupleType, Tuple} from "@synerty/vortexjs";
import {tutorialTuplePrefix} from "../PluginNames";


@addTupleType
export class StringIntTuple extends Tuple {
    public static readonly tupleName = tutorialTuplePrefix + "StringIntTuple";

    //  Description of date1
    id : number;

    //  Description of string1
    string1 : string;

    //  Description of int1
    int1 : number;

    constructor() {
        super(StringIntTuple.tupleName)
    }
}