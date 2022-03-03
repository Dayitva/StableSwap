import SlippageBadge from "./SlippageBadge";

import { useContext, useEffect } from "react";
import { TokenListContext } from "../../contexts/TokenListContext";
import { useSwapCalculation } from "../../hooks/useSwapCalculation";
import config from "../../config";
import SlippageInputBadge from "./SlippageInputBadge";

export default function SlippageCalculator({
  slippages,
  currentSlippage,
  setCurrentSlippage,
  minReturn,
  setMinReturn,
}) {
  const { toValue } = useSwapCalculation();
  const { toToken } = useContext(TokenListContext);

  useEffect(() => {
    setMinReturn(() => {
      return (
        toValue &&
        toValue -
          (currentSlippage * toValue) / 100 -
          (config.fee * toValue) / 100
      );
    });
  }, [toValue, currentSlippage, setMinReturn]);

  return (
    <div className="mt-3">
      <div className="flex items-center justify-between mt-4">
        <div>
          <h1 className="text-md ml-2">Slippage</h1>
        </div>
        <div className="flex items-center justify-end space-x-2">
          {/* For selecting slippage tolerance. */}
          {slippages.map((slippage, index) => (
            <SlippageBadge
              key={index}
              slippage={slippage}
              active={slippage === currentSlippage}
              onClick={() => {
                setCurrentSlippage(slippage);
              }}
            />
          ))}
          <SlippageInputBadge
            slippage={currentSlippage}
            // onClick={(e) => setCurrentSlippage(e.target.value)}
            onChange={(e) => {
              setCurrentSlippage((old) =>
                e.target.value < 30 ? e.target.value : old
              );
              console.log(currentSlippage);
            }}
          />
        </div>
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
          <p>Slippage: </p>
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
    </div>
  );
}
