import React, { createContext, useState } from "react";
// import { BeaconWallet } from "@taquito/beacon-wallet";

const TezosContext = createContext(null);

// const options = {
//   name: 'Swapper',
//   iconUrl: 'https://tezosTezos.io/img/favicon.png',
//   preferredNetwork: 'granadanet',
// };

function TezosProvider(props) {
  const [tezos, setTezos] = useState(null);
  const [address, setAddress] = useState('');

  const providerValues = {
    tezos, 
    setTezos,
    address,
    setAddress
  };

  return (
    <TezosContext.Provider value={providerValues}>
      {props.children}
    </TezosContext.Provider>
  );
}

export {TezosContext, TezosProvider};
