import * as React from "react";
import { bindActionCreators } from "redux";
import * as actions from '../redux/Actions';
import {withRouter} from 'react-router-dom';
import {connect} from 'react-redux';

class DeviceConfig extends React.Component<any, any> {
    baseUrl = "http://localhost:4000";
    constructor(props) {
        super(props);
        this.state = {
            config: JSON.stringify(this.props.appState.configData.toJSON())
        };
    }
    handleChange(event) {
       this.setState({
           config: event.target.value
       });
      }
    handleSubmit() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ master_device_address: this.props.master_device_address, device_config_list: [JSON.parse(this.state.config)] })
        };
        fetch(this.baseUrl + "/set_lan_configs", requestOptions)
            .then(response => response.json())
            .then(() => {
                this.props.closeModal();
            }
        );
    }
    stringifyOtherDevicesOnLAN() {
        let result = "";
        this.state.otherDevicesOnLAN.forEach(
            address => {
                result = result + address + "; "
            }
        );
        return result;
    }
    parseOtherDevicesString(otherDevicesOnLAN) {
        let addresses = otherDevicesOnLAN.split(';').filter(address => address.length > 0);
        this.setState({
            otherDevicesOnLAN: addresses
        });
    }
    render() {
       return (
            <form style={{display: "flex", flexDirection: "column", justifyContent: "space-between"}} onSubmit={this.handleSubmit}>
                <label>
                    <textarea style={{width: "50vw", height: "50vh"}} name="config" value={this.state.config} onChange={this.handleChange.bind(this)}>
                    </textarea>
                </label>
                <input type="submit" value="Submit" />
            </form>
       )
    }
}

const mapStateToProps = (state) => {
    return {
        appState: state
    };
};

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators<any>(actions, dispatch);
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(DeviceConfig));