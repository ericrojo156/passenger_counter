import * as React from 'react';

export default class CloseIcon extends React.Component<any, {}> {
    constructor() {
        super();
    }
    render() {
        return <div onClick={this.props.closeModal.bind(this)}>
            <img src="https://img.icons8.com/ios/50/000000/xbox-x.png"/>
        </div>
    }
}