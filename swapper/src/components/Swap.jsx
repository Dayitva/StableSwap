import React, { useCallback, useContext, useEffect, useState } from "react";
import InputBox from "./swap/InputBox";
import Button from "./forms/Button";
import { TokenListContext } from "../contexts/TokenListContext";
import CONFIG from "../config";
import { LoadingContext } from "../contexts/LoadingContext";

import { debounce } from "lodash";
import { getDy } from "../utils/estimates";
import { toast } from "react-toastify";

import axios from "axios";
import { useSwapCalculation } from "../hooks/useSwapCalculation";
import { exchange, getUserAddress } from "../utils/wallet";
import SlippageBar from "./slippage/SlippageBar";
import TimeSlippageBar from "./slippage/TimeSlippageBar";
import config from "../config";
import { fetchMaxBalanceFA12, fetchMaxBalanceFA2 } from "../utils/balance";
import BigNumber from "bignumber.js";

function Swap() {
  const { changeWhich, setFromToken, setToToken, fromToken, toToken } =
    useContext(TokenListContext);
  const { setShowLoading } = useContext(LoadingContext);

  const slippages = [0.25, 0.5, 1.0];
  const [currentSlippage, setCurrentSlippage] = useState(slippages[0]);
  const [minReturn, setMinReturn] = useState(0);
  const durations = [5, 10, 20];
  const [duration, setDuration] = useState(durations[0]);

  const { fromValue, toValue, setFromValue, setToValue } = useSwapCalculation();
  const giveIJ = () => {
    let i = fromToken.tokenId;
    let j = toToken.tokenId;
    return { i, j };
  };
  //await fetchMaxBalanceFA12("tz1VRTputDyDYy4GjthJqdabKDVxkD3xCYGc", 165890);

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

  async function exchangeTokens() {
    if (!fromValue || !toValue) {
      toast("Invalid Values.");
      return;
    }
    setShowLoading(true);
    const validUpto = new Date(Date.now() + duration * 60 * 1000).toISOString();
    try {
      const data = await exchange(
        fromToken,
        new BigNumber(fromValue).multipliedBy(10 ** fromToken.decimals),
        new BigNumber(minReturn)
          .multipliedBy(10 ** toToken.decimals)
          .toFixed(0),
        validUpto
      );
      setShowLoading(false);
      if (data.success) {
        toast(
          `Successfully Swapped: ${data.hash.slice(0, 5)}...${data.hash.slice(
            data.hash.length - 4,
            data.hash.length
          )}`
        );
      } else {
        toast(data.error);
      }
    } catch (e) {
      setShowLoading(false);
      toast("Error: " + e.message);
    }
  }
  const handleMaxClick = async (type) => {
    let token;
    if (type === "from") {
      token = fromToken;
    } else if (type === "to") {
      token = toToken;
    }

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
      maxBalance = await fetchMaxBalanceFA12(userAddress, token.balanceBigmap);
    }
    console.log(maxBalance);
    if (type === "from") {
      let formattedMaxBalance = new BigNumber(maxBalance).dividedBy(
        10 ** fromToken.decimals
      );
      setFromValue(formattedMaxBalance);
      updateToPrice(formattedMaxBalance);
    } else if (type === "to") {
      let formattedMaxBalance = new BigNumber(maxBalance).dividedBy(
        10 ** toToken.decimals
      );

      setToValue(formattedMaxBalance);
      updateFromPrice(formattedMaxBalance);
    }
  };

  return (
    <div className="bg-gray-900 border-2 border-gray-700 hover:border-gray-600 transition p-2 sm:p-4 rounded-md relative mb-20">
      <div className="flex items-center justify-between border-b border-gray-700 pb-2 mb-3">
        <h1 className="text-sm font-semibold sm:text-lg">Swap</h1>
      </div>
      <div className="space-y-4 mt-2">
        <div>
          <InputBox
            onTokenSwitchClick={() => {
              changeWhich("from");
            }}
            value={fromValue}
            setValue={handleFromChangeEvent}
            token={fromToken}
          />
          <div className="flex justify-end pt-1 pr-1">
            <button
              className="text-xs hover:underline"
              onClick={() => handleMaxClick("from")}
            >
              MAX
            </button>
          </div>
        </div>
        <div>
          <InputBox
            onTokenSwitchClick={() => {
              changeWhich("to");
            }}
            value={toValue}
            setValue={handleToChangeEvent}
            token={toToken}
          />
          <div className="flex justify-end pt-1 pr-1">
            <button
              className="text-xs hover:underline"
              onClick={() => handleMaxClick("to")}
            >
              MAX
            </button>
          </div>
        </div>
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
      <div className="sm:px-2 mt-4">
        <div>
          <h2 className="font-semibold text-sm sm:text-lg mt-3 uppercase">
            Exchange details
          </h2>
        </div>
        <div className="flex justify-between items-center text-xs sm:text-base">
          <p>Fee: </p>
          <p>{config.fee}%</p>
        </div>
        <div className="flex justify-between items-center text-xs sm:text-base">
          <p>Exchange Rate: </p>
          <p>{(toValue / fromValue).toFixed(4)}</p>
        </div>
        <div className="flex justify-between items-center text-xs sm:text-base">
          <p>Price impact: </p>
          <p>{(((fromValue - toValue) / fromValue) * 100).toFixed(4)}%</p>
        </div>
        <div className="flex justify-between items-center text-xs sm:text-base">
          <p>Minimum received: </p>
          <p>
            {minReturn.toFixed(6)} {toToken.symbol}
          </p>
        </div>
      </div>
      <div className="sm:mt-8 mt-3">
        <div className="relative">
          <Button
            text="Swap Tokens"
            bg="w-full sm:text-lg text-xs font-semibold bg-gradient-to-r from-purple-500 to-blue-500"
            padding="sm:py-4 py-3 relative"
            onClick={exchangeTokens}
          />
        </div>
      </div>
    </div>
  );
}

export default Swap;
