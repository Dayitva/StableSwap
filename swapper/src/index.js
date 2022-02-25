import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { TokenListProvider } from "./contexts/TokenListContext";
import { ErrorProvider } from "./contexts/ErrorContext";
import { LoadingProvider } from "./contexts/LoadingContext";
import { WalletProvider } from "./hooks/useWallet";
import { SwapCalculationProvider } from "./hooks/useSwapCalculation";

ReactDOM.render(
  <React.StrictMode>
    <WalletProvider>
      <LoadingProvider>
        <SwapCalculationProvider>
          <ErrorProvider>
            <TokenListProvider>
              <App />
            </TokenListProvider>
          </ErrorProvider>
        </SwapCalculationProvider>
      </LoadingProvider>
    </WalletProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
