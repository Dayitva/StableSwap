import React, { useContext } from "react";
import Error from "./components/error/Error";
import Navbar from "./components/Navbar";
import TokenSelector from "./components/TokenSelector";

// Importing the routes
import Exchange from "./views/Exchange";
import Liquidity from "./views/Liquidity";
import Home from "./views/Home";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { TokenListContext } from "./contexts/TokenListContext";
import Loading from "./components/Loading";
import Faucet from "./views/Faucet";

function App() {
  const { show } = useContext(TokenListContext);

  return (
    <div className="min-h-screen bg-dark relative text-white">
      <BrowserRouter>
        {/* <Navbar /> */}
        {/* Loading component */}
        <Loading />
        {/* Token Selctor for the formToken and ToToken */}
        {show ? (
          <div className="absolute inset-0 bg-black z-50 bg-opacity-90 flex items-start pt-36 justify-center">
            <TokenSelector />
          </div>
        ) : (
          ""
        )}
        <Error />
        <Switch>
          <Route path="/" component={Home} exact />
          {/* <Route path="/exchange" component={Exchange} exact />
          <Route path="/liquidity" component={Liquidity} exact />
          <Route path="/faucet" component={Faucet} exact /> */}
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
