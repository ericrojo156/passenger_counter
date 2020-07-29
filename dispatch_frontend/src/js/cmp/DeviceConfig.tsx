import * as React from "react";
import { bindActionCreators } from "redux";
import * as actions from '../redux/Actions';
import {withRouter} from 'react-router-dom';
import {connect} from 'react-redux';

class DeviceConfig extends React.Component<any, any> {
    constructor(props) {
        super(props);
        this.state = {
            config: JSON.stringify(this.props.appState.configData.toJSON())
        };
    }
    handleChange(event) {
        /*
        const target = event.target;
        const key = target.name;
        let rawValue = target.value;
        let value = rawValue;
        if (key == "otherDevicesOnLAN") {
            value = this.parseOtherDevicesString(rawValue);
        } else if (key == "isMaster" || key == "trackGPS") {
            value = !!parseInt(rawValue);
        } else if (key == "onBoardingDirection") {
            let possibleValues = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
            value = possibleValues[parseInt(rawValue) - 1];
        } else if (key == "dividerLine") {
            value = JSON.parse(rawValue);
        }
        this.setState({[key]: value});
        */
       this.setState({
           config: event.target.value
       });
      }
    handleSubmit() {

    }
    stringifyOtherDevicesOnLAN() {
        let result = "";
        this.state.otherDevicesOnLAN.forEach(
            address => {
                result = result + address + "; "
            }
        )
        return result;
    }
    parseOtherDevicesString(otherDevicesOnLAN) {
        let addresses = otherDevicesOnLAN.split(';').filter(address => address.length > 0);
        this.setState({
            otherDevicesOnLAN: addresses
        })
    }
    render() {
        /*
        return (
            <div style={{backgroundColor: "rgb(255, 255, 255)"}}>
                <form style={{display: "flex", flexDirection: "column", justifyContent: "space-between"}} onSubmit={this.handleSubmit}>
                    <label>
                        Is a Master Device
                        <select name="isMaster" value={this.state.isMaster ? 1 : 0} onChange={this.handleChange.bind(this)}>
                            <option value={1}>YES</option>
                            <option value={0}>NO</option>
                        </select>
                    </label>
                    <label>
                        Other devices on LAN
                        <input style={{width: "30vw"}} name="otherDevicesOnLAN" value={this.stringifyOtherDevicesOnLAN()} onChange={this.handleChange.bind(this)} />
                    </label>
                    <label>
                        Trackable by GPS
                        <select name="trackGPS" value={this.state.trackGPS ? 1 : 0} onChange={this.handleChange.bind(this)}>
                            <option value={1}>YES</option>
                            <option value={0}>NO</option>
                        </select>
                    </label>
                    <label>
                        Allowed Boarding
                        <select multiple={true} name="allowedBoarding" value={this.state.allowedBoarding} onChange={this.handleChange.bind(this)}>
                            <option value={"IN"}>IN</option>
                            <option value={"OUT"}>OUT</option>
                        </select>
                    </label>
                    <label>
                        Onboarding Direction
                        <select name="onBoardingDirection" value={this.state.onBoardingDirection} onChange={this.handleChange.bind(this)}>
                            <option value={1}>[1, 1]</option>
                            <option value={2}>[1, -1]</option>
                            <option value={3}>[-1, 1]</option>
                            <option value={4}>[-1, -1]</option>
                        </select>
                    </label>
                    <label>
                        Divider Line
                        <input style={{width: "30vw"}} type="text" name="dividerLine" value={JSON.stringify(this.state.dividerLine)} onChange={this.handleChange.bind(this)}/>
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        );
        */
       return (
            <form style={{display: "flex", flexDirection: "column", justifyContent: "space-between"}} onSubmit={this.handleSubmit}>
            <label>
                <textarea style={{width: "50vw", height: "50vh"}} name="config" value={this.state.config} onChange={this.handleChange.bind(this)}>
                </textarea>
            </label>
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