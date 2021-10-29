import React, { useContext } from "react";
import Button from "./forms/Button";
// import {connectToWallet} from '../utils/wallet';
import { BeaconWallet } from "@taquito/beacon-wallet";
import { TezosToolkit } from "@taquito/taquito";
import CONFIG from "../config";
import { TezosContext } from "../contexts/TezosContext";
import { ErrorContext } from "../contexts/ErrorContext";
import Jdenticon from "react-jdenticon";
import { NavLink } from "react-router-dom";

const routes = [
  { id: 1, name: "Home", path: "/" },
  { id: 2, name: "Exchange", path: "/exchange" },
  { id: 3, name: "Liquidity", path: "/liquidity" },
  {id: 4, name: "Faucet", path: "/faucet"},
];

function Navbar() {
  const { showMessage } = useContext(ErrorContext);
  const { tezos, setTezos, address, setAddress } = useContext(TezosContext);

  async function connectToWallet() {
    console.log(tezos);
    if (!tezos) {
      const tezos = new TezosToolkit(CONFIG.rpcUrl);
      const options = {
        name: "StableSwap",
        preferredNetwork: CONFIG.preferredNetwork,
      };
      const wallet = new BeaconWallet(options);
      await wallet.requestPermissions({
        network: { type: CONFIG.preferredNetwork },
      });
      tezos.setWalletProvider(wallet);
      const pkh = await tezos.wallet.pkh();
      setTezos(tezos);
      setAddress(pkh);
    } else {
      showMessage("💳️ Wallet is already connected.");
      console.log("Already there.");
    }
  }

  return (
    <div className="fixed left-0 right-0 top-0 h-16 shadow-md border-b-2 border-gray-900 z-40 bg-dark">
      <nav className="flex items-center container mx-auto h-full justify-between">
        <h1 className="font-semibold uppercase text-lg text-gray-200">
          🔄 Liquibrium
        </h1>
        <div>
          <ul className="flex items-center space-x-10 text-sm">
            {routes.map((route) => {
              return (
                <li key={route.id}>
                  <NavLink
                    to={route.path}
                    className="text-gray-400 hover:text-gray-100"
                  >
                    {route.name}
                  </NavLink>
                </li>
              );
            })}
          </ul>
        </div>
        <div className="flex items-center space-x-2">
          {address ? <Jdenticon size="42" value={address} /> : ""}
          <Button
            text={
              tezos
                ? `${address.slice(0, 5)}...${address.slice(32, 36)}`
                : "CONNECT"
            }
            bg="bg-gradient-to-r from-purple-500 to-blue-500"
            onClick={connectToWallet}
          />
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
