import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { TokenListProvider } from "./contexts/TokenListContext";
import { TezosProvider } from "./contexts/TezosContext";
import { ErrorProvider } from "./contexts/ErrorContext";
import { LoadingProvider } from "./contexts/LoadingContext";

ReactDOM.render(
  <React.StrictMode>
    <LoadingProvider>
      <ErrorProvider>
        <TokenListProvider>
          <TezosProvider>
            <App />
          </TezosProvider>
        </TokenListProvider>
      </ErrorProvider>
    </LoadingProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
