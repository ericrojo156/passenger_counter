import * as React from 'react';
import {DEVICE_CONFIG} from "../redux/Actions";
export default class ConfigIcon extends React.Component<any,{}> {
    baseUrl = "http://localhost:4000";
    defaultConfig = {"isMaster": false, "otherDevicesOnLAN": [], "trackGPS": true, "allowedBoarding": ["IN", "OUT"], "dividerLine": {"equation": {"a": 1, "b": 0, "order": 1}, "onBoardingDirection": [1, 1]}}
    constructor() {
        super();
    }
    goToConfig() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ master_device_address: this.props.master_device_address })
        };
        fetch(this.baseUrl + "/get_lan_configs", requestOptions)
            .then(response => response.json())
            .then(data => {
                let selectedConfig = data.device_config_list.find(
                    config => config.id == this.props.id
                );
                this.props.hydrateConfigData(this.props.id, selectedConfig || this.defaultConfig)
                this.props.setModalContent(DEVICE_CONFIG)
            }
        );
    }
    render() {
        return (
            <div onClick={this.goToConfig.bind(this)}>
                <img src="https://img.icons8.com/cotton/64/000000/settings--v1.png"/>
            </div>
        )
    }
}