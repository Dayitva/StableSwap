import React, { useCallback, useContext, useEffect, useState } from "react";
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
import SlippageBar from "./slippage/SlippageBar";
import TimeSlippageBar from "./slippage/TimeSlippageBar";
import config from "../config";

function Swap() {
  const { changeWhich, setFromToken, setToToken, fromToken, toToken } =
    useContext(TokenListContext);
  const { setShowLoading } = useContext(LoadingContext);

  const slippages = [0.25, 0.5, 1.0];
  const [currentSlippage, setCurrentSlippage] = useState(slippages[0]);
  const [minReturn, setMinReturn] = useState(0);
  const durations = [1, 5, 10, 20];
  const [duration, setDuration] = useState(durations[0]);

  const { fromValue, toValue, setFromValue, setToValue } = useSwapCalculation();
  const giveIJ = () => {
    let i = fromToken.tokenId;
    let j = toToken.tokenId;
    return { i, j };
  };
  useEffect(() => {
    setMinReturn(() => {
      return (
        toValue &&
        toValue -
          (currentSlippage * toValue) / 100 -
          (config.fee * toValue) / 100
      );
    });
  }, [currentSlippage, fromValue, toValue]);

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

  async function exchangeTokens() {
    setShowLoading(true);
    const validUpto = new Date(Date.now() + duration * 60 * 1000).toISOString();
    const data = await exchange(
      fromToken,
      parseInt(fromValue * 10 ** fromToken.decimals),
      parseInt(minReturn * 10 ** toToken.decimals),
      validUpto
    );
  }

  return (
    <div className="bg-gray-900 border-2 border-gray-700 hover:border-gray-600 transition p-4 rounded-md relative">
      <div className="flex items-center justify-between border-b border-gray-700 pb-2 mb-3">
        <h1 className="text-lg">Swap</h1>
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
      <div>
        <SlippageBar
          slippages={slippages}
          currentSlippage={currentSlippage}
          setCurrentSlippage={setCurrentSlippage}
        />
      </div>
      <div>
        <TimeSlippageBar
          durations={durations}
          currentDuration={duration}
          setCurrentDuration={setDuration}
          time={true}
        />
      </div>
      <div className="px-2">
        {/* Div to show calculations. */}
        <div>
          <h2 className="font-semibold text-lg mt-3 uppercase">Calculations</h2>
        </div>
        <div className="flex justify-between items-center">
          <p>Fee: </p>
          <p>
            {((config.fee * toValue) / 100).toFixed(6)} {toToken.symbol}
          </p>
        </div>
        <div className="flex justify-between items-center">
          <p>Price impact: </p>
          <p>
            {((currentSlippage * toValue) / 100).toFixed(6)} {toToken.symbol}
          </p>
        </div>
        <div className="flex justify-between items-center">
          <p>Minimum returns: </p>
          <p>
            {minReturn.toFixed(6)} {toToken.symbol}
          </p>
        </div>
      </div>
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
