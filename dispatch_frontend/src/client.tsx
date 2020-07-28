import * as React from "react";
import ReactDOM from "react-dom";
import {createStore} from 'redux';
import State from './js/redux/Reducers';
import {Provider} from 'react-redux'
import "babel-polyfill";

const app = document.getElementById('app');
let store = createStore(State);

ReactDOM.render(
	<Provider store={store}>
				<div className="rootDiv">
                    <div style={{marginTop: '5vw'}}>
                        APP CONTENT!
                    </div>
				</div>
	</Provider>,
	app);
