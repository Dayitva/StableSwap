// This is the homepage.
import React from "react";
import PoolStats from "../components/PoolStats";
import Swap from "../components/Swap";

function Exchange() {
  return (
    <div className="px-4">
      <div className="pt-16 mt-20">
        {/* Main Content Goes Here... */}
        <div className="mx-auto max-w-xl relative">
          <PoolStats />
        </div>
        <div className="mt-8 mx-auto max-w-xl relative">
          {/* Wrapper for swap component... */}
          {/* <div className="absolute -inset-0.5 bg-gray-800 blur"></div> */}
          <Swap />
        </div>
      </div>
    </div>
  );
}

export default Exchange;
