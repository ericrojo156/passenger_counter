import * as React from "react";

export default class DeviceConfig extends React.Component<any,{}> {
    constructor() {
        super();
    }
    render() {
        return (
            <div>
                {this.props.appState.configData}
            </div>
        );
    }
}