import React, { useContext, useState } from 'react';
import InputBox from './swap/InputBox';
import Button from './forms/Button';
import {TokenListContext} from '../contexts/TokenListContext';
import {TezosContext} from '../contexts/TezosContext';
// import {tokenList} from '../utils/tokenList';
import {RefreshIcon, CalculatorIcon} from '@heroicons/react/outline';
import {getDecimals} from '../utils/wallet';

function Swap() {
  const {changeWhich, setFromToken, setToToken, fromToken, toToken} = useContext(TokenListContext);
  const {tezos} = useContext(TezosContext);
  const handleInterChange = () => {
    const oldFromToken = fromToken
    setFromToken(toToken)
    setToToken(oldFromToken)
  }
  function calculateOutTokens() {
    if (!tezos) {return 0}
    const decimals = getDecimals(tezos, fromToken.address);
    console.log(decimals)
  }
  
  const [fromValue, setFromValue] = useState(0);
  const [toValue, setToValue] = useState(0);

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
          onTokenSwitchClick={()=>{changeWhich('from')}} 
          value={fromValue}
          setValue={setFromValue}
          token={fromToken}
        />
        <InputBox 
          onTokenSwitchClick={()=>{changeWhich('to')}} 
          value={toValue}
          setValue={setToValue}
          token={toToken}
        />
      </div>
      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button text="Swap Tokens" bg="w-full bg-blue-500" padding="py-4 relative"/>
        </div>
      </div>
    </div>
  )
}

export default Swap
