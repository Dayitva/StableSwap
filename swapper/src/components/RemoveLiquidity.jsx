import { useState, useContext, useCallback, useEffect } from "react";
import PlainInputBox from "./PlainInputBox";
import Button from "./forms/Button";
import { ErrorContext } from "../contexts/ErrorContext";
import CONFIG from "../config";

import { debounce } from "lodash";
import axios from "axios";
import { estimateTokensByLp } from "../utils/estimates";
import config from "../config";
import { removeLiquidity } from "../utils/wallet";
import BigNumber from "bignumber.js";
import SlippageBar from "./slippage/SlippageBar";
import { toast } from "react-toastify";
import { LoadingContext } from "../contexts/LoadingContext";
import { getUserAddress } from "../utils/wallet";
import { fetchMaxBalanceFA12, fetchMaxBalanceFA2 } from "../utils/balance";

function RemoveLiquidity() {
  const slippages = [0.25, 0.5, 1.0];
  const [lpAmount, setLpAmount] = useState(0);
  const [slippage, setSlippage] = useState(slippages[0]);
  const { setShowLoading } = useContext(LoadingContext);
  const [outTokens, setOutTokens] = useState({
    0: 0,
    1: 0,
  });

  useEffect(() => {
    setOutTokens((o) => {
      return {
        0: o[0] - (slippage * o[0]) / 100,
        1: o[1] - (slippage * o[1]) / 100,
      };
    });
  }, [slippage, lpAmount]);

  function handleChangeLpEvent(lpValue) {
    setLpAmount(lpValue);
    debounceSave(lpValue);
  }
  async function updateOutTokens(newValue) {
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );
    let tokenPool = [
      new BigNumber(data.token_pool[0].pool).minus(
        new BigNumber(data.token_pool[0].admin_fee)
      ),
      new BigNumber(data.token_pool[1].pool).minus(
        new BigNumber(data.token_pool[1].admin_fee)
      ),
    ];
    let tokenAmount = estimateTokensByLp(
      tokenPool,
      new BigNumber(newValue).multipliedBy(new BigNumber(10 ** 18)),
      new BigNumber(data.lp_supply)
    );
    console.log({
      0: tokenAmount[0],
      1: tokenAmount[1],
    });
    setOutTokens({
      0: tokenAmount[0].toFixed(),
      1: tokenAmount[1].toFixed(),
    });
    // setOutTokens(tokenAmount);
  }
  const debounceSave = useCallback(
    // eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateOutTokens(newValue), 1000),
    []
  );

  async function handleRemoveLiquidity() {
    if (!lpAmount) {
      toast("Invalid Values.");
      return;
    }
    try {
      setShowLoading(true);
      console.log(
        new BigNumber(lpAmount).multipliedBy(
          new BigNumber("1000000000000000000")
        ),
        1,
        1
      );
      const data = await removeLiquidity(
        new BigNumber(lpAmount).multipliedBy(
          new BigNumber("1000000000000000000")
        ),
        new BigNumber(outTokens[0]).dividedToIntegerBy(
          new BigNumber(10 ** (18 - config.tokens[0].decimals))
        ),
        new BigNumber(outTokens[1]).dividedToIntegerBy(
          new BigNumber(10 ** (18 - config.tokens[1].decimals))
        )
      );
      setShowLoading(false);

      if (data.success) {
        toast(
          `Successfully Removed Liquidity: ${data.hash.slice(
            0,
            5
          )}...${data.hash.slice(data.hash.length - 4, data.hash.length)}`
        );
      } else {
        toast(data.error);
      }
    } catch (e) {
      setShowLoading(false);
      toast(`Error: ${e.message}`);
    }
  }
  const handleMaxClick = async () => {
    let token = config.lpToken;

    const isFA2 = token.isFA2;
    const userAddress = await getUserAddress();
    let maxBalance = 0;
    if (isFA2) {
      maxBalance = await fetchMaxBalanceFA2(
        userAddress,
        token.balanceBigmap,
        0
      );
    } else {
      console.log("fetch max balance");
      maxBalance = await fetchMaxBalanceFA12(userAddress, token.balanceBigmap);
    }
    console.log("Max Balance", maxBalance);
    const maxFormattedBalance = new BigNumber(maxBalance)
      .dividedBy(new BigNumber(10 ** 18))
      .toFixed();
    setLpAmount(maxFormattedBalance);
    updateOutTokens(maxFormattedBalance);
    console.log("Check the decimals, ", maxFormattedBalance);
  };

  return (
    <div className="rounded-md relative">
      <div className="space-y-4 mt-2">
        <div>
          <PlainInputBox
            label={"Amount of LP tokens"}
            value={lpAmount}
            setValue={handleChangeLpEvent}
            type={"number"}
          />
          <div className="flex justify-end pt-1 pr-1">
            <button
              className="text-xs hover:underline"
              onClick={() => handleMaxClick()}
            >
              MAX
            </button>
          </div>
        </div>
        <div>
          <div className="mb-3">
            <SlippageBar
              slippages={slippages}
              currentSlippage={slippage}
              setCurrentSlippage={setSlippage}
            />
          </div>
          <h2 className="text-md sm:text-xl font-semibold">
            Estimated Tokens:
          </h2>
          <p className="text-gray-100 flex items-center justify-between text-xs sm:text-base">
            <span>Amount of kUSD:</span>{" "}
            <span className="font-medium"> {outTokens[0] / 10 ** 18} kUSD</span>
          </p>
          <p className="text-gray-100 flex items-center justify-between text-xs sm:text-base">
            <span>Amount of wUSDC:</span>{" "}
            <span className="font-medium">{outTokens[1] / 10 ** 18} wUSDC</span>
          </p>
        </div>
      </div>

      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Remove Liquidity"
            bg="w-full sm:text-lg text-xs font-semibold bg-gradient-to-r from-purple-500 to-blue-500"
            padding="sm:py-4 py-3 relative"
            onClick={handleRemoveLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default RemoveLiquidity;
