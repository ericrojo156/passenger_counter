import * as React from "react";

export default class Device extends React.Component<any,{}> {
    constructor(props) {
        super(props);
    }
    openModal() {
        this.props.openModal(this.props.id);
    }
    render() {
        return (
            <div style={{backgroundColor: "rgb(255, 255, 255)", display: 'flex', flexDirection: 'row', height: '10vh', width: '50vw', alignItems: 'center', justifyContent: 'space-evenly', border: '5px solid black'}} onClick={this.openModal.bind(this)}>
                <div style={{flexDirection: 'column'}}>
                    LABEL
                    <div>{this.props.device_label}</div>
                </div>
                <div style={{flexDirection: 'column'}}>
                    PASSENGERS COUNT
                    <div>{this.props.count}</div>
                </div>
                <div style={{flexDirection: 'column'}}>
                    LATITUDE
                    <div>{this.props.gps.lat}</div>
                </div>
                <div style={{flexDirection: 'column'}}>
                    LONGITUDE
                    <div>{this.props.gps.lng}</div>
                </div>
            </div>
        )
    }
}