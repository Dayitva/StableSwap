import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import {TokenListProvider} from './contexts/TokenListContext';
import {TezosProvider} from './contexts/TezosContext';

ReactDOM.render(
  <React.StrictMode>
    <TokenListProvider>
      <TezosProvider>
        <App />
      </TezosProvider>
    </TokenListProvider>
  </React.StrictMode>,
  document.getElementById('root')
)
