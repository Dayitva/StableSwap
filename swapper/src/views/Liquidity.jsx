import React, { useContext, useEffect, useState } from "react";
import AddLiquidity from "../components/AddLiquidity";
import Balances from "../components/Balances";
import RemoveLiquidity from "../components/RemoveLiquidity";
import { TezosContext } from "../contexts/TezosContext";
import CONFIG from "../config";
import axios from 'axios'

function Liquidity() {
  const [kusdAmount, setKusdAmount] = useState(0.0);
  const [usdtzAmount, setUsdtzAmount] = useState(0.0);
  const [lpamount, setLpAmount] = useState(0.0);

  const {address, tezos} = useContext(TezosContext); 

  /**
   * 
   * @param {User Address} userAddress 
   * @param {Bigmap Id of FA1.2 token} bigmapId 
   * @returns balance of the user.
   */
  async function getBalance(userAddress, bigmapId) {
    const {data} = await axios.get(
      `https://api.granadanet.tzkt.io/v1/bigmaps/${bigmapId}/keys`
    );
    const requiredEl = data.find((el) => {
      return el.key === userAddress;
    })
    if (requiredEl) {
      return parseInt(requiredEl.value.balance);
    } else {
      return 0;
    }
  }

  useEffect(() => {
    async function updateBalances() {
      if (tezos) {
        const lp = await getBalance(
          address,
          CONFIG.lpBigmapId
        );
        setLpAmount(lp);
  
        const usdtz = await getBalance(
          address,
          CONFIG.usdtzBigmapId
        );
        setUsdtzAmount(usdtz);
  
        const kusd = await getBalance(
          address,
          CONFIG.kusdBigmapId
        )
        setKusdAmount(kusd)
        console.log({usdtz, kusd, lp})
      }
    }
    
    fireHook();
    async function fireHook() {
      await updateBalances();
    }
  }, [address, tezos])

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
