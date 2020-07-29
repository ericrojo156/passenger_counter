import Vehicles from "../views/Vehicles";
import DeviceConfig from "./DeviceConfig";
import {withRouter} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import * as actions from '../redux/Actions';
import {connect} from 'react-redux';

const mapStateToProps = (state) => {
    return {
        appState: state
    };
};

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators<any>(actions, dispatch);
};

export const vehicles = withRouter(connect(mapStateToProps, mapDispatchToProps)(Vehicles));