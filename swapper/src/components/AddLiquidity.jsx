import React, { useContext, useState } from "react";
import { ErrorContext } from "../contexts/ErrorContext";
import { TokenListContext } from "../contexts/TokenListContext";
import InputBox from "../components/swap/InputBox";
import Button from "../components/forms/Button";
import { LoadingContext } from "../contexts/LoadingContext";
import { addLiquidity } from "../utils/wallet";

function AddLiquidity() {
  const { changeWhich, fromToken } = useContext(TokenListContext);
  const [fromValue, setFromValue] = useState(0);
  const { showMessage } = useContext(ErrorContext);
  const { setShowLoading } = useContext(LoadingContext);

  async function provideLiquidity() {
    setShowLoading(true);
    try {
      const data = await addLiquidity(
        fromToken,
        parseInt(fromValue * 10 ** fromToken.decimals)
      );
      showMessage(`✅ ${data.hash}`);
    } catch (error) {
      showMessage(`🔃 ${error.message}`);
      setShowLoading(false);
    }
  }

  return (
    <div>
      <div className="space-y-4 mt-2">
        <InputBox
          onTokenSwitchClick={() => {
            changeWhich("from");
          }}
          value={fromValue}
          setValue={setFromValue}
          token={fromToken}
        />
      </div>
      <div className="mt-4">
        <div className="relative">
          {/* <div className="absolute inset-0 bg-blue-500 blur"></div> */}
          <Button
            text="Add Liquidity"
            bg="w-full text-lg bg-gradient-to-r from-purple-500 to-blue-500"
            padding="py-4 relative"
            onClick={provideLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default AddLiquidity;
