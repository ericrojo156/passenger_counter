import * as React from "react";
import { bindActionCreators } from "redux";
import * as actions from '../redux/Actions';
import {withRouter} from 'react-router-dom';
import {connect} from 'react-redux';

class DeviceConfig extends React.Component<any,{}> {
    constructor() {
        super();
    }
    render() {
        return (
            <div>
                CONFIG DATA HERE
            </div>
        );
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