import * as React from "react";
import Device from "../cmp/Device"

export default class Vehicles extends React.Component<any,{}> {
    baseUrl = "http://localhost:4000";
    refreshHandler;
    constructor(props) {
        super(props);
    }
    componentDidMount() {
        this.refreshHandler = setInterval(this.refresh.bind(this), 1000);
    }
    componentWillUnmount() {
        clearInterval(this.refreshHandler);
    }
    refresh() {
            fetch(this.baseUrl + "/refresh")
            .then(response => response.json())
            .then(data => {
                const vehicles = Object.values(data.data);
                this.props.refresh(vehicles);
            }
        );
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
                        return <Device id={vehicleJSON.id} device_label={vehicleJSON.device_label} count={vehicleJSON.master_device.passenger_count} gps={vehicleJSON.master_device.gps_coords} openModal={this.openVehicleModal.bind(this)}/>
                    }
                )}
            </div>
        )

    }
}