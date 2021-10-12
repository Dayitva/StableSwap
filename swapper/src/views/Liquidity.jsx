import React, { useContext, useState } from "react";
import AddLiquidity from "../components/AddLiquidity";
import Balances from "../components/Balances";
import RemoveLiquidity from "../components/RemoveLiquidity";

function Liquidity() {
  const [kusdAmount, setKusdAmount] = useState(0.0);
  const [usdtzAmount, setUsdtzAmount] = useState(0.0);
  const [lpamount, setLpAmount] = useState(0.0);

  return (
    <div>
      <div className="pt-16">
        {/* The balance Component */}
        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <Balances 
            kusdAmount={kusdAmount}
            lpAmount={lpamount}
            usdTzAmount={usdtzAmount}
          />
        </div>
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
