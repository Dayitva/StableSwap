import React, { useContext } from "react";
import { ErrorContext } from "../contexts/ErrorContext";
import { TezosContext } from "../contexts/TezosContext";
import { TokenListContext } from "../contexts/TokenListContext";
import AddLiquidity from "../components/AddLiquidity";

function Liquidity() {
  return (
    <div>
      <div className="pt-16">
        {/* Main Content Goes Here... */}
        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <div className="absolute -inset-0.5 bg-gray-800 blur"></div>
          <AddLiquidity />
        </div>
      </div>
    </div>
  );
}

export default Liquidity;
