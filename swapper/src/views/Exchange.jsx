// This is the homepage.
import React, { useContext } from "react";
import Swap from "../components/Swap";

function Exchange() {
  return (
    <div>
      <div className="pt-16">
        {/* Main Content Goes Here... */}
        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <div className="absolute -inset-0.5 bg-gray-800 blur"></div>
          <Swap />
        </div>
      </div>
    </div>
  );
}

export default Exchange;
