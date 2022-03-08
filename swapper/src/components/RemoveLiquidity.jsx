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

function RemoveLiquidity() {
  const slippages = [0.25, 0.5, 1.0];
  const [lpAmount, setLpAmount] = useState(0);
  const [slippage, setSlippage] = useState(slippages[0]);
  const { showMessage } = useContext(ErrorContext);
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
  }, [slippage]);

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
      new BigNumber(newValue * 10 ** 18),
      new BigNumber(data.lp_supply)
    );
    console.log({
      0: tokenAmount[0].toFixed(6),
      1: tokenAmount[1].toFixed(6),
    });
    setOutTokens({
      0: parseFloat(tokenAmount[0].toFixed(6)),
      1: parseFloat(tokenAmount[1].toFixed(6)),
    });
    // setOutTokens(tokenAmount);
  }
  const debounceSave = useCallback(
    // eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateOutTokens(newValue), 1000),
    []
  );

  async function handleRemoveLiquidity() {
    console.log(
      parseInt(lpAmount * 10 ** 18),
      parseInt(outTokens[0]) / 10 ** (18 - config.tokens[0].decimals),
      parseInt(outTokens[1]) / 10 ** (18 - config.tokens[1].decimals)
    );
    const data = await removeLiquidity(
      parseInt(lpAmount * 10 ** 18),
      parseInt(parseInt(outTokens[0]) / 10 ** (18 - config.tokens[0].decimals)),
      parseInt(parseInt(outTokens[1]) / 10 ** (18 - config.tokens[1].decimals))
    );
  }

  return (
    <div className="rounded-md relative">
      <div className="space-y-4 mt-2">
        <PlainInputBox
          label={"Amount of LP tokens"}
          value={lpAmount}
          setValue={handleChangeLpEvent}
          type={"number"}
        />
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
