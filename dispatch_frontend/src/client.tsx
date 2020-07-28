import * as React from "react";
import ReactDOM from "react-dom";
import {createStore} from 'redux';
import State from './js/redux/Reducers';
import {Provider} from 'react-redux'
import "babel-polyfill";
import Vehicles from "./js/views/Vehicles"
const app = document.getElementById('app');
let store = createStore(State);

ReactDOM.render(
	<Provider store={store}>
				<div className="rootDiv">
                    <div style={{marginTop: '5vw'}}>
                        <Vehicles />
                    </div>
				</div>
	</Provider>,
	app);
