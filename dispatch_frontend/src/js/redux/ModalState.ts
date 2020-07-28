import * as Immutable from "immutable";

export const modalStateDefault = Immutable.Map<string, any>({
    "isOpen": false,
    "modalType": "",
    "vehicle": Immutable.List<any>([]),
    "config": {}
});