import * as Immutable from 'immutable';

export const vehicleStateDefault = Immutable.Map<string, Immutable.Map<string, any>>({
        "1": Immutable.Map<string, any>({master_device_address: "http://localhost:3000", id: "1", label: "master1", count: 5, gps: {lat: "1234", lng: "4321"}, devices: Immutable.List<Immutable.Map<string, any>>([
            Immutable.Map<string, any>({id: "1a", label: "slave1a", count: 5, gps: {lat: "1234", lng: "4321"}}),
            Immutable.Map<string, any>({id: "1b", label: "slave1b", count: 5, gps: {lat: "1234", lng: "4321"}})
        ])}),
        "2": Immutable.Map<string, any>({master_device_address: "http://localhost:3005", id: "2", label: "master2", count: 10, gps: {lat: "6789", lng: "7890"}, devices: Immutable.List<Immutable.Map<string, any>>([
            Immutable.Map<string, any>({id: "2a", label: "slave2a", count: 5, gps: {lat: "6789", lng: "7890"}}),
            Immutable.Map<string, any>({id: "2b", label: "slave2b", count: 5, gps: {lat: "6789", lng: "7890"}})
        ])})
});