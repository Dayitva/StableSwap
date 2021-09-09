import React, {useContext} from 'react'
import {ChevronDownIcon} from '@heroicons/react/solid';

function TokenSwitch({click, token}) {
  return (
    <button 
      className="flex items-center space-x-1 bg-gray-900 px-2 py-1 rounded-full focus:outline-none"
      onClick={click}
    >
      <img 
        src={token.imageUrl}
        className="w-6 h-6"
      />
      <span className="text-sm">{token.symbol}</span>
      <ChevronDownIcon className="w-6 h-6" />
    </button>
  )
}

export default TokenSwitch
