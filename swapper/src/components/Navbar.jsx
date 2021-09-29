import React, {useContext} from "react";
import Button from './forms/Button';
// import {connectToWallet} from '../utils/wallet';
import {BeaconWallet} from '@taquito/beacon-wallet';
import {TezosToolkit} from '@taquito/taquito';
import CONFIG from '../config';
import {TezosContext} from '../contexts/TezosContext';
import { ErrorContext } from "../contexts/ErrorContext";




function Navbar() {
  const {showMessage} = useContext(ErrorContext);
  const {tezos, setTezos, address, setAddress} = useContext(TezosContext);

  async function connectToWallet() {
    console.log(tezos)
    if (!tezos) {
      const tezos = new TezosToolkit(CONFIG.rpcUrl);
      const options = {
        name: 'StableSwap',
        preferredNetwork: CONFIG.preferredNetwork,
      }
      const wallet = new BeaconWallet(options);
      await wallet.requestPermissions({
        network: {type: CONFIG.preferredNetwork}
      });
      tezos.setWalletProvider(wallet);
      const pkh = await tezos.wallet.pkh();
      setTezos(tezos);
      setAddress(pkh);
    } else {
      showMessage("💳️ Wallet is already connected.")
      console.log('Already there.')
    }
  }

  return (
    <div className="fixed left-0 right-0 top-0 h-16 shadow-md border-b-2 border-gray-900">
      <nav className="flex items-center container mx-auto h-full justify-between">
        <h1 className="font-semibold uppercase text-lg text-gray-200">
          🔄 StableSwap
        </h1>
        <div>
          <ul className="flex items-center space-x-10 text-sm">
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">Home</a></li>
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">About Us</a></li>
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">Docs</a></li>
          </ul>
        </div>
        <div>
          <Button 
            text={ tezos ? `${address.slice(0, 5)}...${address.slice(32, 36)}` :  "CONNECT" }
            bg="bg-gradient-to-r from-purple-500 to-blue-500"
            onClick={connectToWallet}
          />
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
