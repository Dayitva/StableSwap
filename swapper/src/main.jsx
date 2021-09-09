import React from 'react'
import ReactDOM from 'react-dom'
import './static/css/index.css'
import App from './App'
import {TokenListProvider} from './contexts/TokenListContext';

ReactDOM.render(
  <React.StrictMode>
    <TokenListProvider>
      <App />
    </TokenListProvider>
  </React.StrictMode>,
  document.getElementById('root')
)
