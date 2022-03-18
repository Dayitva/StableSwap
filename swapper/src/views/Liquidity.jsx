import React, { useEffect, useCallback } from "react";
import CONFIG from "../config";
import axios from "axios";
import PoolStats from "../components/PoolStats";
import useWallet from "../hooks/useWallet";
import LiquidityTab from "../components/liquidity";
import Navbar from "../components/Navbar";

function Liquidity() {
  const { wallet } = useWallet();

  async function getBalance(userAddress, bigmapId) {
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/bigmaps/${bigmapId}/keys`
    );
    const requiredEl = data.find((el) => {
      return el.key === userAddress;
    });
    if (requiredEl) {
      return parseInt(requiredEl.value.balance);
    } else {
      return 0;
    }
  }

  const updateBalances = useCallback(async () => {
    if (wallet) {
      const lp = await getBalance(wallet, CONFIG.lpBigmapId);

      const usdtz = await getBalance(wallet, CONFIG.usdtzBigmapId);

      const kusd = await getBalance(wallet, CONFIG.kusdBigmapId);
      console.log({ usdtz, kusd, lp });
    }
  }, [wallet]);

  useEffect(() => {
    updateBalances();
  }, [updateBalances]);

  return (
    <div>
      <Navbar />
      <div className=" mx-auto max-w-xl pt-20 px-4">
        <div className="mt-8 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <PoolStats />
        </div>
        {/* Main Content Goes Here... */}
        <div className="sm:mt-20 mt-6 mx-auto max-w-2xl relative mb-20">
          <LiquidityTab />
        </div>
      </div>
    </div>
  );
}

export default Liquidity;
