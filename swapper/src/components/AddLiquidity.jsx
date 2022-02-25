import React, { useContext, useState } from "react";
import { ErrorContext } from "../contexts/ErrorContext";
import { TokenListContext } from "../contexts/TokenListContext";
import InputBox from "../components/swap/InputBox";
import Button from "../components/forms/Button";
import CONFIG from "../config";
import { LoadingContext } from "../contexts/LoadingContext";
import { TezosToolkit } from "@taquito/taquito";
import config from "../config";

function AddLiquidity() {
  const { changeWhich, fromToken } = useContext(TokenListContext);
  const [fromValue, setFromValue] = useState(0);
  const { showMessage } = useContext(ErrorContext);
  const { setShowLoading } = useContext(LoadingContext);

  async function provideLiquidity() {
    setShowLoading(true);
    try {
      const tezos = new TezosToolkit(config.rpcUrl);
      const liquidityTokenContract = await tezos.wallet.at(fromToken.address);
      const stableSwapContract = await tezos.wallet.at(
        CONFIG.StableSwapAddress
      );

      const amount = parseInt(fromValue * 10 ** fromToken.decimals);

      const batch = await tezos.wallet
        .batch()
        .withContractCall(
          liquidityTokenContract.methods.approve(
            CONFIG.StableSwapAddress,
            amount
          )
        )
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
