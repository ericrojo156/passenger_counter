import * as React from "react";
import ReactDOM from "react-dom";
import {createStore} from 'redux';
import State from './js/redux/Reducers';
import {Provider} from 'react-redux'
import "babel-polyfill";
import ModalDialog from "./js/cmp/ModalDialog"
import {browserHistory, Switch, Route} from 'react-router';
import {BrowserRouter} from 'react-router-dom';
import {
	vehicles
} from './js/cmp/ComponentsForRouter';
const app = document.getElementById('app');
let store = createStore(State);

ReactDOM.render(
	<Provider store={store}>
		<BrowserRouter history={browserHistory}>
				<div className="rootDiv">
					<ModalDialog />
                    <div style={{marginTop: '5vw'}}>
						<Switch>
							<Route exact path="/" component={vehicles}/>
						</Switch>
                    </div>
				</div>
		</BrowserRouter>
	</Provider>,
	app);
