import React, { useCallback, useContext, useEffect, useState } from "react";
import { TokenListContext } from "../contexts/TokenListContext";
import InputBox from "../components/swap/InputBox";
import Button from "../components/forms/Button";
import { LoadingContext } from "../contexts/LoadingContext";
import { addLiquidity } from "../utils/wallet";
import SlippageBar from "./slippage/SlippageBar";
import { debounce } from "lodash";
import { estimateLP } from "../utils/estimates";
import axios from "axios";
import CONFIG from "../config";
import { toast } from "react-toastify";

function AddLiquidity() {
  const slippages = [0.25, 0.5, 1.0];
  const [slippage, setSlippage] = useState(slippages[0]);

  const { changeWhich, fromToken } = useContext(TokenListContext);
  const [fromValue, setFromValue] = useState(0);
  const { setShowLoading } = useContext(LoadingContext);
  const [outLP, setOutLP] = useState(0);
  const [min, setMin] = useState(0);

  useEffect(() => {
    if (!outLP) {
      setMin(0);
    }
    setMin(outLP - (outLP * slippage) / 100);
  }, [slippage, outLP]);

  async function provideLiquidity() {
    if (!fromValue) {
      toast("Invalid Values.");
      return;
    }
    try {
      setShowLoading(true);
      const data = await addLiquidity(
        fromToken,
        parseInt(fromValue * 10 ** fromToken.decimals),
        parseInt(min * 10 ** fromToken.decimals)
      );
      setShowLoading(false);
      if (data.success) {
        toast(
          `Successfully Added Liquidity: ${data.hash.slice(
            0,
            5
          )}...${data.hash.slice(data.hash.length - 4, data.hash.length)}`
        );
      } else {
        toast(data.error);
      }
    } catch (error) {
      console.log(error);
      setShowLoading(false);
      toast(`Error: ${error.message}`);
    }
  }

  const handleValueChange = (value) => {
    setFromValue(value);
    debounceSave(value);
  };
  const debounceSave = useCallback(
    debounce((val) => updateValue(val), 1000),
    []
  );
  const updateValue = async (val) => {
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );

    let tokenPool = [
      parseInt(parseInt(data.token_pool[0].pool) / 10 ** 18),
      parseInt(parseInt(data.token_pool[1].pool) / 10 ** 18),
    ];
    let e = estimateLP(tokenPool, parseInt(val), fromToken, parseInt(data.A));
    console.log(`Estimated LP pool tokens`, e);
    setOutLP(e);
  };

  return (
    <div>
      <div className="space-y-4 mt-2">
        <InputBox
          onTokenSwitchClick={() => {
            changeWhich("from");
          }}
          value={fromValue}
          setValue={handleValueChange}
          token={fromToken}
          type={"number"}
        />
      </div>
      <div>
        <div className="mb-3">
          <SlippageBar
            slippages={slippages}
            currentSlippage={slippage}
            setCurrentSlippage={setSlippage}
          />
        </div>
        <h2 className="text-md sm:text-xl mt-3">Estimated Tokens:</h2>
        <p className="text-gray-100 flex items-center justify-between text-xs sm:text-base">
          <span>Minimum LP recieve:</span>{" "}
          <span className="font-medium"> {min || 0} LLP</span>
        </p>
      </div>
      <div className="mt-4">
        <div className="relative">
          <Button
            text="Add Liquidity"
            bg="w-full sm:text-lg text-xs font-semibold bg-gradient-to-r from-purple-500 to-blue-500"
            padding="sm:py-4 py-3 relative"
            onClick={provideLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default AddLiquidity;
