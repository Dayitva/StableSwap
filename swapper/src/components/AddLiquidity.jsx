import React, { useContext, useState } from "react";
import { ErrorContext } from "../contexts/ErrorContext";
import { TezosContext } from "../contexts/TezosContext";
import { TokenListContext } from "../contexts/TokenListContext";
import InputBox from "../components/swap/InputBox";
import Button from "../components/forms/Button";
import CONFIG from "../config";
import { LoadingContext } from "../contexts/LoadingContext";

function AddLiquidity() {
  const { changeWhich, fromToken } = useContext(TokenListContext);
  const [fromValue, setFromValue] = useState(0);
  const { tezos } = useContext(TezosContext);
  const { showMessage } = useContext(ErrorContext);
  const { setShowLoading } = useContext(LoadingContext);

  async function provideLiquidity() {
    setShowLoading(true);
    try {
      const liquidityTokenContract = await tezos.wallet.at(fromToken.address);
      const stableSwapContract = await tezos.wallet.at(
        CONFIG.StableSwapAddress
      );

      const amount = parseInt(fromValue) * 10 ** fromToken.decimals;

      const batch = await tezos.wallet
        .batch()
        .withContractCall(
          stableSwapContract.methods.add_liquidity(amount, fromToken.tokenId)
        );

      const batchOp = await batch.send();
      setShowLoading(false);
      console.log("Operation Hash: ", batchOp.opHash);
      showMessage(`✅ ${batchOp.opHash}`);
      await batchOp.confirmation();
    } catch (error) {
      showMessage(`🔃 ${error.message}`);
      setShowLoading(false);
    }
  }

  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center justify-between">
        <h1>Add Liquidity</h1>

        {/* The below div is not needed */}
        {/* <div className="space-x-2">
          <button onClick={handleInterChange}>
            <RefreshIcon className="w-5 h-5" />
          </button>
          <button onClick={calculateOutTokens}>
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
          setValue={setFromValue}
          token={fromToken}
        />
      </div>
      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Add Liquidity"
            bg="w-full bg-blue-500"
            padding="py-4 relative"
            onClick={provideLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default AddLiquidity;
