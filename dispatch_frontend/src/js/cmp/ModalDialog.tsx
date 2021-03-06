import * as React from 'react';
import Modal from 'react-modal';
import {withRouter} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import * as actions from '../redux/Actions';
import {connect} from 'react-redux';
import Device from './Device';
import ConfigIcon from "./ConfigIcon";
import DeviceConfig from "./DeviceConfig";
import CloseIcon from "./CloseIcon";
class ModalDialog extends React.Component<any, {}> {

    style;

    constructor() {
        super();
        this.style = {
            overlay : {
                position          : 'fixed',
                top               : 0,
                left              : 0,
                right             : 0,
                bottom            : 0,
                backgroundColor   : 'rgba(255, 255, 255, 0.75)',
                zIndex            : 300
            },
            content : {
                position                   : 'fixed',
                top                        : '5%',
                left                       : '5%',
                right                      : '5%',
                bottom                     : '5%',
                background                 : 'rgba(1, 1, 1, 0.50)',
                overflow                   : 'auto',
                WebkitOverflowScrolling    : 'touch',
                outline                    : 'none',
                padding                    : '5%',
                display                    : 'flex',
                flexDirection              : 'row',
                justifyContent             : 'center',
                alignItems                 : 'center',
                height                     : '85vh',
                width                      : '75vw'
            }
        };
    }
    closeModal() {
        this.props.closeModal();
    }
    renderModalContent(vehicle) {
            let contentType = this.props.appState.modalData.get("contentType");
            if (contentType == actions.VEHICLES_MODAL && vehicle.size > 0) {
                return (
                    <div>
                        <div>
                            {vehicle.get("label")}
                        </div>
                        <div>
                            {vehicle.get("doors").map(
                                device => {
                                    let device_label = device.device_label;
                                    let device_state = device.device_state
                                    return (
                                        <div style={{display: 'flex', flexDirection: 'row'}}>
                                            <Device id={device_state.id} device_label={device_label} count={device_state.passenger_count} gps={device_state.gps_coords} openVehicleModal={null}/>
                                            <ConfigIcon id={device_state.id} setModalContent={this.props.setModalContent.bind(this)} hydrateConfigData={this.props.hydrateConfigData.bind(this)} master_device_address={vehicle.get("master_device_address")}/>
                                        </div>
                                    )
                                }
                            )}
                        </div>
                    </div>
                );
            } else if (contentType == actions.DEVICE_CONFIG) {
                return <DeviceConfig config={this.props.appState.configData}/>
            }
            else {
                return <div>MODAL IN ERROR STATE</div>
            }
    }
    render() {
        const shouldShowModal = this.props.appState.modalData.get("isOpen");
        const vehicle = this.props.appState.modalData.get("vehicle");
        return (
            <div>
                <Modal
                    isOpen={!!shouldShowModal}
                    style={this.style}
                    contentLabel="modal"
                    shouldCloseOnOverlayClick={true}
                    shouldCloseOnEsc={true}
                >
                    {this.renderModalContent(vehicle)}
                    <CloseIcon closeModal={this.props.closeModal.bind(this)} />
                </Modal>
            </div>
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ModalDialog));