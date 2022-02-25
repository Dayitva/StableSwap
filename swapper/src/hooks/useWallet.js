import React, { createContext, useContext } from "react";

export const walletContext = createContext(null);

const useWallet = () => useContext(walletContext);

export const WalletProvider = (props) => {
  const [wallet, setWallet] = React.useState(null);

  const contextValues = { wallet, setWallet };
  return (
    <walletContext.Provider value={contextValues}>
      {props.children}
    </walletContext.Provider>
  );
};

export default useWallet;
