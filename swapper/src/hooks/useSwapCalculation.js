import React, { useState, useContext } from "react";

export const SwapCalculationContext = React.createContext({});
export const useSwapCalculation = () => useContext(SwapCalculationContext);

export const SwapCalculationProvider = (props) => {
  const [fromValue, setFromValue] = useState(0);
  const [toValue, setToValue] = useState(0);

  return (
    <SwapCalculationContext.Provider
      value={{ fromValue, toValue, setFromValue, setToValue }}
    >
      {props.children}
    </SwapCalculationContext.Provider>
  );
};
