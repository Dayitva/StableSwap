import React from "react";
import Button from "./forms/Button";
import Jdenticon from "react-jdenticon";
import { NavLink } from "react-router-dom";
import { ArrowRightIcon, MenuIcon, XIcon } from "@heroicons/react/outline";

import { useEffect, useState } from "react";
import {
  connectWallet,
  disconnectWallet,
  getActiveAccount,
} from "../utils/wallet";
import useWallet from "../hooks/useWallet";

const routes = [
  { id: 1, name: "Home", path: "/" },
  { id: 2, name: "Exchange", path: "/exchange" },
  { id: 3, name: "Liquidity", path: "/liquidity" },
  { id: 4, name: "Faucet", path: "/faucet" },
];

function Navbar() {
  const { wallet, setWallet } = useWallet();
  const [mobileNav, setMobileNav] = useState(false);

  const handleConnectWallet = async () => {
    const { wallet } = await connectWallet();
    setWallet(wallet);
  };
  const handleDisconnectWallet = async () => {
    const { wallet } = await disconnectWallet();
    setWallet(wallet);
  };

  useEffect(() => {
    const func = async () => {
      const account = await getActiveAccount();
      if (account) {
        setWallet(account.address);
      }
    };
    func();
  }, [setWallet]);

  return (
    <div className="fixed left-0 right-0 top-0 sm:h-24 h-16 shadow-md border-b-2 border-gray-900 z-40 bg-dark">
      <nav className="relative flex items-stretch container mx-auto h-full justify-between px-4">
        <div className="flex items-center justify-center">
          <img src="/assets/logo.png" alt="Logo" className="h-24 sm:h-44" />
        </div>
        <div
          className={`absolute md:static md:block top-full left-0 right-0 bg-black ${
            !mobileNav ? "hidden" : "block"
          }`}
        >
          <ul className="block md:flex md:h-full text-sm">
            {routes.map((route) => {
              return (
                <NavLink
                  key={route.id}
                  to={route.path}
                  className="h-full flex md:items-center justify-between md:justify-center hover:bg-gray-900 text-gray-400 hover:text-gray-100 px-6 transition-all duration-200 py-5"
                >
                  <li key={route.id}>{route.name}</li>
                  <ArrowRightIcon className="w-5 h-5 md:hidden" />
                </NavLink>
              );
            })}
          </ul>
        </div>
        <div className="flex items-center space-x-4">
          {wallet ? <Jdenticon size="42" value={wallet} /> : ""}
          <Button
            text={
              wallet
                ? `${wallet.slice(0, 5)}...${wallet.slice(32, 36)}`
                : "CONNECT"
            }
            bg="bg-gradient-to-r from-purple-500 to-blue-500 font-semibold"
            onClick={!wallet ? handleConnectWallet : handleDisconnectWallet}
          />
          <button
            onClick={() => {
              setMobileNav(!mobileNav);
            }}
            className="md:hidden bg-gray-800 p-2 rounded-sm"
          >
            {mobileNav ? (
              <XIcon className="w-5 h-5" />
            ) : (
              <MenuIcon className="w-5 h-5" />
            )}
          </button>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
