import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { TokenListProvider } from "./contexts/TokenListContext";
import { TezosProvider } from "./contexts/TezosContext";
import { ErrorProvider } from "./contexts/ErrorContext";

ReactDOM.render(
  <React.StrictMode>
    <ErrorProvider>
      <TokenListProvider>
        <TezosProvider>
          <App />
        </TezosProvider>
      </TokenListProvider>
    </ErrorProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
