import React, { useContext } from "react";
import AddLiquidity from "../components/AddLiquidity";
import RemoveLiquidity from "../components/RemoveLiquidity";

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

        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <div className="absolute -inset-0.5 bg-gray-800 blur"></div>
          <RemoveLiquidity />
        </div>
      </div>
    </div>
  );
}

export default Liquidity;
