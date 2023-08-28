import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import SignIn from './Sign-in';
import reportWebVitals from './reportWebVitals';
import { UserContextProvider } from './components/UserContext';
import Home from './home';
import {
  BrowserRouter,
  Route,
  Routes
} from "react-router-dom";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
<BrowserRouter>
<ThemeProvider theme={darkTheme}>
  <CssBaseline />
    <React.StrictMode>
      <UserContextProvider>
        <Routes>
          <Route path="/" element={<React.Fragment><SignIn /></React.Fragment>} />
          <Route path="/home" element={<React.Fragment><Home /></React.Fragment>} />
        </Routes>
      </UserContextProvider>
    </React.StrictMode>
    </ThemeProvider>
  </BrowserRouter>
);

reportWebVitals();
