import React, { useContext, useState } from "react";
import InputBox from "./swap/InputBox";
import Button from "./forms/Button";
import { TokenListContext } from "../contexts/TokenListContext";
import { TezosContext } from "../contexts/TezosContext";
import { RefreshIcon, CalculatorIcon } from "@heroicons/react/outline";
import { getDecimals } from "../utils/wallet";
import CONFIG from "../config";
import { ErrorContext } from "../contexts/ErrorContext";

function Swap() {
  const { changeWhich, setFromToken, setToToken, fromToken, toToken } =
    useContext(TokenListContext);
  const { showMessage } = useContext(ErrorContext);
  const { tezos } = useContext(TezosContext);
  const [fromValue, setFromValue] = useState(0);
  const [toValue, setToValue] = useState(0);

  const handleInterChange = () => {
    const oldFromToken = fromToken;
    setFromToken(toToken);
    setToToken(oldFromToken);
  };
  function calculateOutTokens() {
    // if (!tezos) {
    //   return 0;
    // }
    const decimals = getDecimals(tezos, fromToken.address);
    console.log(decimals);
  }

  async function exchangeTokens() {
    try {
      const fromTokenContract = await tezos.wallet.at(fromToken.address);
      const stableSwapContract = await tezos.wallet.at(
        CONFIG.StableSwapAddress
      );
      const amount = parseInt(fromValue) * 10 ** fromToken.decimals;
      console.log(`Amount to exchange: ${amount} ${typeof amount}`);
      const batch = await tezos.wallet
        .batch()
        // .withContractCall(fromTokenContract.methods.approve(
        //   CONFIG.StableSwapAddress,
        //   fromValue * 10 ** fromToken.decimals
        // ))
        .withContractCall(
          stableSwapContract.methods.exchange(
            amount,
            fromToken.tokenId,
            toToken.tokenId
          )
        );

      const batchOp = await batch.send();
      console.log("Operation hash:", batchOp.hash);
      await batchOp.confirmation();
    } catch (err) {
      showMessage(err.message);
      console.log(err);
    }

    // tezos.wallet
    //   .at(CONFIG.StableSwapAddress)
    //   .then((contract) => {
    //       return contract.methods.exchange(
    //         fromToken.tokenId,
    //         toToken.tokenId,
    //         fromValue * 10 ** fromToken.decimals
    //       ).send()
    //     }
    //   )
    //   .then((op) => {
    //     console.log(`OpHash:`, op.opHash)
    //     return op.confirmation();
    //   })
    //   .then((result) => {
    //     console.log(result)
    //     if (result.completed) {
    //       console.log(`Transaction correctly processed!
    //       Block: ${result.block.header.level}
    //       Chain ID: ${result.block.chain_id}`);
    //     } else {
    //       console.log('An error has occurred');
    //     }
    //   })
    // // const op = contract.methods.exchange(
    //   fromToken.tokenId,
    //   toToken.tokenId,
    //   fromValue * 10 ** fromToken.decimals
    // ).send();
    // console.log(op.opHash)
    // const result = await op.confirmation();
    // if (result.completed) {
    //   console.log(`Transaction correctly processed!
    //   Block: ${result.block.header.level}
    //   Chain ID: ${result.block.chain_id}`);
    // } else {
    //   console.log('An error has occurred');
    // }
  }

  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center justify-between">
        <h1>Swap</h1>
        <div className="space-x-2">
          <button onClick={handleInterChange}>
            <RefreshIcon className="w-5 h-5" />
          </button>
          <button onClick={calculateOutTokens}>
            <CalculatorIcon className="w-5 h-5" />
          </button>
        </div>
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
        <InputBox
          onTokenSwitchClick={() => {
            changeWhich("to");
          }}
          value={toValue}
          setValue={setToValue}
          token={toToken}
        />
      </div>
      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Swap Tokens"
            bg="w-full bg-blue-500"
            padding="py-4 relative"
            onClick={exchangeTokens}
          />
        </div>
      </div>
    </div>
  );
}

export default Swap;
