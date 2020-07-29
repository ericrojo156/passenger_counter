import * as Immutable from 'immutable';
import {combineReducers} from 'redux';
import { vehicleStateDefault } from './VehicleState';
import { modalStateDefault } from './modalState';
import { configDataDefault } from './ConfigState';
import { REFRESH, OPEN_MODAL, CLOSE_MODAL, HYDRATE_CONFIG_DATA, SET_MODAL_CONTENT } from './Actions';
const vehicles = (vehiclesState: Immutable.Map<string, any> = vehicleStateDefault, action: any) => {
    switch (action.type) {
        case REFRESH:
            action.vehicles.forEach(vehicle => {
                let latest_record = vehicle.latest_record;
                latest_record["master_device_address"] = vehicle.master_device_address;
                vehiclesState = vehiclesState.setIn([vehicle.id], Immutable.Map<string, any>(latest_record));
            });
            return vehiclesState;
        default:
            return vehiclesState;
    }
}

const modalData = (modalState: Immutable.Map<string, any> = modalStateDefault, action: any) => {
    switch (action.type) {
        case OPEN_MODAL:
            modalState = modalState.setIn(["isOpen"], true);
            modalState = modalState.setIn(["vehicle"], Immutable.Map<string, any>(action.vehicle));
            return modalState;
        case CLOSE_MODAL:
            modalState = modalStateDefault;
            return modalState;
        case SET_MODAL_CONTENT:
            modalState = modalState.setIn(["contentType"], action.contentType);
            return modalState;
        default:
            return modalState;
    }
}

const configData = (configDataState: Immutable.Map<string, any> = configDataDefault, action: any) => {
    switch (action.type) {
        case HYDRATE_CONFIG_DATA:
            configDataState = Immutable.Map<string, any>(action.config)
            return configDataState;
        default:
            return configDataState;
    }
}

const State = combineReducers({
    vehicles, modalData, configData
});

export default State;