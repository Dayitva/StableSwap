import { useState, useContext, useCallback } from 'react';
import PlainInputBox from './PlainInputBox';
import Button from './forms/Button';
import { ErrorContext } from "../contexts/ErrorContext";
import { TezosContext } from '../contexts/TezosContext';
import CONFIG from '../config';

import { debounce } from 'lodash';
import axios from 'axios';
import { estimateTokensByLp } from '../utils/estimates';

function RemoveLiquidity() {
  const [lpAmount, setLpAmount] = useState(0);
  const { showMessage } = useContext(ErrorContext);
  const {tezos} = useContext(TezosContext);
  const [outTokens, setOutTokens] = useState({0: 0, 1: 0});
  
  function handleChangeLpEvent(lpValue) {
    setLpAmount(lpValue);
    debounceSave(lpValue);
  }
  async function updateOutTokens(newValue) {
    const {data} = await axios.get(
      `https://api.granadanet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    )
    let tokenPool = [
      parseInt(data.token_pool[0].pool), 
      parseInt(data.token_pool[1].pool),
    ]
    let tokenAmount = estimateTokensByLp(tokenPool, newValue);
    setOutTokens(tokenAmount);
  }
  const debounceSave = useCallback(// eslint-disable-line react-hooks/exhaustive-deps
    debounce((newValue) => updateOutTokens(newValue), 1000),
    []
  )


  async function removeLiquidity() {
    const stableSwapContract = await tezos.wallet.at(CONFIG.StableSwapAddress);
    const amount = parseInt(lpAmount * 10 ** 9);
    const op = await stableSwapContract.methods.remove_liquidity(amount).send();
    showMessage(`✅ ${op.opHash}`)
    const result = op.confirmation();
    console.log(result);
  }


  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center justify-between">
        <h1>Remove Liquidity</h1>
      </div>
      <div className="space-y-4 mt-2">
        <PlainInputBox
          label={"Amount of LP tokens"}
          value={lpAmount}
          setValue={handleChangeLpEvent}
        />
        <div>
        <p className="text-gray-300 text-sm">Estimated Tokens:</p>
        <p className="text-gray-300 text-xs ml-2">KUSD: {outTokens[0]}</p>
        <p className="text-gray-300 text-xs ml-2">USDtz: {outTokens[1]}</p>
        </div>
        
      </div>

      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Remove Liquidity"
            bg="w-full bg-blue-500"
            padding="py-4 relative"
            onClick={removeLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default RemoveLiquidity;