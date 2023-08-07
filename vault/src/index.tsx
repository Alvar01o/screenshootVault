import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import SignIn from './Sign-in';
import reportWebVitals from './reportWebVitals';
import {IUser} from './interfaces'

const initializeUser: IUser = {
  name: '',
  email: '',
}

const loggerUser = React.createContext<IUser>(initializeUser)

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <SignIn />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
