import { vehicles } from "../cmp/ComponentsForRouter";

export const REFRESH = "refresh";
export const OPEN_MODAL = "modalIsOpen";
export const CLOSE_MODAL = "closeModal";
export const HYDRATE_CONFIG_DATA = "hydrateConfigData";
export const SET_MODAL_CONTENT = "setModalContent";
export const DEVICE_CONFIG = "deviceConfig";
export const VEHICLES_MODAL = "vehiclesModal";

export function refresh(vehicles) {
    return ({type: REFRESH, vehicles: vehicles});
}

export function openModal(vehicle) {
    return ({type: OPEN_MODAL, vehicle: vehicle});
}

export function closeModal() {
    return ({type: CLOSE_MODAL})
}

export function hydrateConfigData(id, config) {
    return ({type: HYDRATE_CONFIG_DATA, id: id, config: config});
}

export function setModalContent(contentType) {
    return ({type: SET_MODAL_CONTENT, contentType: contentType})
}