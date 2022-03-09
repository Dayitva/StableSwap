import React, { createContext, useEffect, useState } from "react";
import config from "../config";
const tokenList = config.tokens;

const TokenListContext = createContext(false);

function TokenListProvider(props) {
  const [show, setShow] = useState(false);
  const [fromToken, setFromToken] = useState(tokenList[0]);
  const [toToken, setToToken] = useState(tokenList[1]);
  const [which, setWhich] = useState("");
  const [list, setList] = useState(tokenList);

  useEffect(() => {
    if (toToken === fromToken) {
      if (toToken.id === 1) {
        setToToken(tokenList[1]);
      } else {
        setToToken(tokenList[0]);
      }
    }
  }, [fromToken, toToken]);

  const changeWhich = (newValue) => {
    if (newValue === "from") {
      setWhich("from");
    } else {
      setWhich("to");
    }
    setShow(true);
  };
  const setToken = (newTokenValue) => {
    if (which === "from") {
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
    which,
    list,
    setList,
  };

  return (
    <TokenListContext.Provider value={providerValues}>
      {props.children}
    </TokenListContext.Provider>
  );
}

export { TokenListContext, TokenListProvider };
