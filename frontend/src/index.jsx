import React from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.min.css';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

document.documentElement.setAttribute('data-color-mode', 'light');

const consoleError = console.error.bind(console);

// eslint-disable-next-line
console.error = (errObj, ...args) => {

  if (process.env.NODE_ENV === 'development' && typeof errObj === 'string' && args.includes('findDOMNode')) {
    return;
  }
  consoleError(errObj, ...args);
};

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
