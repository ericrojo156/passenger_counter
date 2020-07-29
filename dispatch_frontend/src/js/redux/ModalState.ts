import * as Immutable from "immutable";
import { VEHICLES_MODAL } from "./Actions";

export const modalStateDefault = Immutable.Map<string, any>({
    "isOpen": false,
    "contentType": VEHICLES_MODAL,
    "vehicle": Immutable.List<any>([]),
    "config": {}
});