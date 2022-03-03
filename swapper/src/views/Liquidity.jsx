import React, { useEffect, useCallback } from "react";
import CONFIG from "../config";
import axios from "axios";
import PoolStats from "../components/PoolStats";
import useWallet from "../hooks/useWallet";
import LiquidityTab from "../components/liquidity";

function Liquidity() {
  const { wallet } = useWallet();
  // const [kusdAmount, setKusdAmount] = useState(0);
  // const [usdtzAmount, setUsdtzAmount] = useState(0);
  // const [lpamount, setLpAmount] = useState(0);

  /**
   *
   * @param {User Address} userAddress
   * @param {Bigmap Id of FA1.2 token} bigmapId
   * @returns balance of the user.
   */
  async function getBalance(userAddress, bigmapId) {
    const { data } = await axios.get(
      `https://api.granadanet.tzkt.io/v1/bigmaps/${bigmapId}/keys`
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
      // setLpAmount(lp);

      const usdtz = await getBalance(wallet, CONFIG.usdtzBigmapId);
      // setUsdtzAmount(usdtz);

      const kusd = await getBalance(wallet, CONFIG.kusdBigmapId);
      // setKusdAmount(kusd);
      console.log({ usdtz, kusd, lp });
    }
  }, [wallet]);

  useEffect(() => {
    updateBalances();
  }, [updateBalances]);

  return (
    <div>
      <div className=" mx-auto max-w-xl pt-20">
        {/* The balance Component */}
        {/* <div className="mt-20 mx-auto max-w-2xl relative">
          <Balances
            kusdAmount={kusdAmount}
            lpAmount={lpamount}
            usdTzAmount={usdtzAmount}
          />
        </div> */}

        <div className="mt-8 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <PoolStats />
        </div>
        {/* Main Content Goes Here... */}
        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          {/* <div className="absolute -inset-0.5 bg-gray-800 blur"></div> */}
          <LiquidityTab />
        </div>
      </div>
    </div>
  );
}

export default Liquidity;
