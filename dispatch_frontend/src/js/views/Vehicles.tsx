import * as React from "react";
import Device from "../cmp/Device"

export default class Vehicles extends React.Component<any,{}> {
    constructor() {
        super();
    }
    openVehicleModal(id) {
        if (this.props.openModal != null) {
            let vehicle = this.props.appState.vehicles.toArray().find(v => v.get("id") == id);
            this.props.openModal.bind(this)(vehicle);
        }
    }
    render() {
        const vehicles = this.props.appState.vehicles.toArray();
        return (
            <div style={{display: 'flex', flexDirection: 'column', height: '100vh', alignItems: "center", justifyContent: 'flex-start', border: '5px solid black'}}>
                VEHICLES
                {vehicles.map(
                    vehicle => {
                        const vehicleJSON = vehicle.toJSON();
                        return <Device id={vehicleJSON.id} label={vehicleJSON.label} count={vehicleJSON.count} gps={vehicleJSON.gps} openModal={this.openVehicleModal.bind(this)}/>
                    }
                )}
            </div>
        )

    }
}