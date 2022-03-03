import React, { useCallback, useContext, useState } from "react";
import InputBox from "./swap/InputBox";
import Button from "./forms/Button";
import { TokenListContext } from "../contexts/TokenListContext";
// import { RefreshIcon, CalculatorIcon } from "@heroicons/react/outline";
import CONFIG from "../config";
// import { ErrorContext } from "../contexts/ErrorContext";
import { LoadingContext } from "../contexts/LoadingContext";

import { debounce } from "lodash";
import { getDy } from "../utils/estimates";

import axios from "axios";
import SlippageCalculator from "./slippage/SlippageCalculator";
import { useSwapCalculation } from "../hooks/useSwapCalculation";
import { exchange } from "../utils/wallet";

function Swap() {
  const { changeWhich, setFromToken, setToToken, fromToken, toToken } =
    useContext(TokenListContext);
  // const { showMessage } = useContext(ErrorContext);
  const { setShowLoading } = useContext(LoadingContext);

  const slippages = [0.25, 0.5, 1.0];
  const [currentSlippage, setCurrentSlippage] = useState(slippages[0]);
  const [minReturn, setMinReturn] = useState(0);

  // const [fromValue, setFromValue] = useState(0);
  // const [toValue, setToValue] = useState(0);
  const { fromValue, toValue, setFromValue, setToValue } = useSwapCalculation();
  const giveIJ = () => {
    let i = fromToken.tokenId;
    let j = toToken.tokenId;
    return { i, j };
  };

  const debounceSave = useCallback(
    // eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateToPrice(newValue), 1000),
    [fromToken, toToken]
  );

  const debounceToSave = useCallback(
    // eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateFromPrice(newValue), 1000),
    [fromToken, toToken]
  );
  function handleFromChangeEvent(newValue) {
    setFromValue(newValue);
    debounceSave(newValue);
  }
  function handleToChangeEvent(newValue) {
    setToValue(newValue);
    debounceToSave(newValue);
  }
  async function updateFromPrice(toValue) {
    console.log(fromToken, toToken);
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );
    let tokenPool = [
      parseInt(data.token_pool[0].pool) / 10 ** 18,
      parseInt(data.token_pool[1].pool) / 10 ** 18,
    ];
    let { i, j } = giveIJ();
    let N_COINS = 2;
    let dx = parseFloat(toValue);
    let A = parseInt(data.A);
    let fromValue = getDy(tokenPool, i, j, dx, A, N_COINS);
    console.log({ data, i, j, N_COINS, dx, A, toValue });
    setFromValue(fromValue || 0);
  }

  async function updateToPrice(fromValue) {
    console.log(fromToken.tokenId, toToken.tokenId);

    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );
    console.log("Hello Worl");
    let tokenPool = [
      parseInt(data.token_pool[0].pool) / 10 ** 18,
      parseInt(data.token_pool[1].pool) / 10 ** 18,
    ];
    let { i, j } = giveIJ();
    let N_COINS = 2;
    let dx = parseFloat(fromValue);
    let A = parseInt(data.A);
    let toValue = getDy(tokenPool, i, j, dx, A, N_COINS);
    console.log("After calculating dy");
    console.log({ data, i, j, N_COINS, dx, A, toValue });
    setToValue(toValue || 0);
  }

  const handleInterChange = () => {
    const oldFromToken = fromToken;
    setFromToken(toToken);
    setToToken(oldFromToken);
  };
  // function calculateOutTokens() {
  //   // if (!tezos) {
  //   //   return 0;
  //   // }
  //   const decimals = getDecimals(tezos, fromToken.address);
  //   console.log(decimals);
  // }

  async function exchangeTokens() {
    // try {
    setShowLoading(true);
    const validUpto = new Date(Date.now() + 60000).toISOString();
    const data = await exchange(
      fromToken,
      parseInt(fromValue * 10 ** fromToken.decimals),
      parseInt(minReturn * 10 ** toToken.decimals),
      validUpto
    );
    // } catch (err) {
    //   setShowLoading(false);
    //   showMessage(err.message);
    //   console.log(err);
    // }
  }

  return (
    <div className="bg-gray-900 border-2 border-gray-700 hover:border-gray-600 transition p-4 rounded-md relative">
      <div className="flex items-center justify-between border-b border-gray-700 pb-2 mb-3">
        <h1 className="text-lg">Swap</h1>
        {/* <div className="space-x-2">
          <button onClick={handleInterChange}>
            <RefreshIcon className="w-5 h-5" />
          </button>
          <button>
            <CalculatorIcon className="w-5 h-5" />
          </button>
        </div> */}
      </div>
      <div className="space-y-4 mt-2">
        <InputBox
          onTokenSwitchClick={() => {
            changeWhich("from");
          }}
          value={fromValue}
          setValue={handleFromChangeEvent}
          token={fromToken}
        />
        <InputBox
          onTokenSwitchClick={() => {
            changeWhich("to");
          }}
          value={toValue}
          setValue={handleToChangeEvent}
          token={toToken}
        />
      </div>
      <SlippageCalculator
        slippages={slippages}
        currentSlippage={currentSlippage}
        setCurrentSlippage={setCurrentSlippage}
        minReturn={minReturn}
        setMinReturn={setMinReturn}
      />
      <div className="mt-8">
        <div className="relative">
          {/* <div className="absolute inset-0 bg-blue-500 blur"></div> */}
          <Button
            text="Swap Tokens"
            bg="w-full text-lg bg-gradient-to-r from-purple-500 to-blue-500"
            padding="py-4 relative"
            onClick={exchangeTokens}
          />
        </div>
      </div>
    </div>
  );
}

export default Swap;
