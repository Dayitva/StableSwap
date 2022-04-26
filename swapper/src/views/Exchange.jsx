// This is the homepage.
import React from "react";
import PoolStats from "../components/PoolStats";
import Swap from "../components/Swap";
import Navbar from "../components/Navbar";
import Balance from "../components/Balance";
import useWallet from "../hooks/useWallet";

function Exchange() {
  const { wallet } = useWallet();
  return (
    <div className="px-4">
      <Navbar />
      <div className="pt-20 mt-20">
        <div className="mx-auto max-w-xl relative">
          <PoolStats />
        </div>
        <div className="mx-auto max-w-xl relative mt-4">
          {wallet && <Balance />}
        </div>
        <div className="mt-8 mx-auto max-w-xl relative">
          <Swap />
        </div>
      </div>
    </div>
  );
}

export default Exchange;
