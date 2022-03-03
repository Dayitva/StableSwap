import { useState, useContext, useCallback } from "react";
import PlainInputBox from "./PlainInputBox";
import Button from "./forms/Button";
import { ErrorContext } from "../contexts/ErrorContext";
import CONFIG from "../config";

import { debounce } from "lodash";
import axios from "axios";
import { estimateTokensByLp } from "../utils/estimates";
import config from "../config";
import { TezosToolkit } from "@taquito/taquito";
import { removeLiquidity } from "../utils/wallet";

function RemoveLiquidity() {
  const [lpAmount, setLpAmount] = useState(0);
  const { showMessage } = useContext(ErrorContext);
  const [outTokens, setOutTokens] = useState({ 0: 0, 1: 0 });

  function handleChangeLpEvent(lpValue) {
    setLpAmount(lpValue);
    debounceSave(lpValue);
  }
  async function updateOutTokens(newValue) {
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );
    let tokenPool = [
      parseInt(parseInt(data.token_pool[0].pool) / 10 ** 18),
      parseInt(parseInt(data.token_pool[1].pool) / 10 ** 18),
    ];
    let adminFee = [
      parseInt(parseInt(data.token_pool[0].admin_fee) / 10 ** 18),
      parseInt(parseInt(data.token_pool[1].admin_fee) / 10 ** 18),
    ];
    let tokenAmount = estimateTokensByLp(
      tokenPool,
      adminFee,
      parseInt(newValue),
      parseInt(parseInt(data.lp_supply) / 10 ** 18)
    );
    console.log(tokenAmount);
    setOutTokens(tokenAmount);
  }
  const debounceSave = useCallback(
    // eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateOutTokens(newValue), 1000),
    []
  );

  async function handleRemoveLiquidity() {
    console.log(parseInt(outTokens[0]), parseInt(outTokens[1]));
    console.log(outTokens);
    const data = await removeLiquidity(
      lpAmount,
      parseInt(outTokens[0] * 10 ** config.tokens[0].decimals),
      parseInt(outTokens[1] * 10 ** config.tokens[1].decimals)
    );
  }

  return (
    <div className="rounded-md relative">
      {/* <div className="flex items-center justify-between">
        <h1>Remove Liquidity</h1>
      </div> */}
      <div className="space-y-4 mt-2">
        <PlainInputBox
          label={"Amount of LP tokens"}
          value={lpAmount}
          setValue={handleChangeLpEvent}
          type={"number"}
        />
        <div>
          <h2 className="text-xl">Estimated Tokens:</h2>
          <p className="text-gray-100 flex items-center justify-between">
            <span>Amount of kUSD:</span>{" "}
            <span className="font-medium"> {outTokens[0]} kUSD</span>
          </p>
          <p className="text-gray-100 flex items-center justify-between">
            <span>Amount of wUSDC:</span>{" "}
            <span className="font-medium">{outTokens[1]} wUSDC</span>
          </p>
        </div>
      </div>

      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Remove Liquidity"
            bg="w-full text-lg bg-gradient-to-r from-purple-500 to-blue-500"
            padding="py-4 relative"
            onClick={handleRemoveLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default RemoveLiquidity;
