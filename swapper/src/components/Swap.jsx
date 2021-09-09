import React, { useContext, useEffect } from 'react'
import InputBox from './swap/InputBox';
import Button from './forms/Button';
import {TokenListContext} from '../contexts/TokenListContext';
import {tokenList} from '../utils/tokenList';
import {RefreshIcon} from '@heroicons/react/outline'

function Swap() {
  const {changeWhich, setFromToken, setToToken, fromToken, toToken} = useContext(TokenListContext);
  const handleInterChange = () => {
    const oldFromToken = fromToken
    setFromToken(toToken)
    setToToken(oldFromToken)
  }
  
  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center justify-between">
        <h1>Swap</h1>
        <button onClick={handleInterChange}>
          <RefreshIcon className="w-5 h-5" />
        </button>
      </div>
      <div className="space-y-4 mt-2">
        <InputBox 
          onTokenSwitchClick={()=>{changeWhich('from')}} 
          token={fromToken}
        />
        <InputBox 
          onTokenSwitchClick={()=>{changeWhich('to')}} 
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
