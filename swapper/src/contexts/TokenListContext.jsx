/* Global State Variable to show/hide TokenList */
import React, { createContext, useState } from "react";
import {tokenList} from '../utils/tokenList';

// `false` here is default value which mean the List will be hidden.
const TokenListContext = createContext(false);

function TokenListProvider(props) {
  const [show, setShow] = useState(false);
  const [fromToken, setFromToken] = useState(tokenList[0]);
  const [toToken, setToToken] = useState(tokenList[1]);
  const [which, setWhich] = useState("from");
  const changeWhich = (newValue) => {
    if (newValue === "from") {
      setWhich("from");
    } else {
      setWhich("to");
    }
    setShow(true);
  };
  const setToken = (newTokenValue) => {
    if (which === 'from') {
      setFromToken(newTokenValue);
    } else {
      setToToken(newTokenValue);
    }
    setShow(false);
  };
  const providerValues = {
    show,
    setShow,
    fromToken,
    toToken,
    setFromToken,
    setToToken,
    setToken,
    changeWhich,
    which
  };

  return (
    <TokenListContext.Provider value={providerValues}>
      {props.children}
    </TokenListContext.Provider>
  );
}

export { TokenListContext, TokenListProvider };
