import React from "react";
import { ChevronDownIcon } from "@heroicons/react/solid";

function TokenSwitch({ click, token }) {
  return (
    <button
      className="flex items-center space-x-1 bg-gray-900 hover:bg-gray-700 px-2 py-1 rounded-full focus:outline-none transition"
      onClick={click}
    >
      <img src={token.imageUrl} className="w-6 h-6" alt={token.symbol} />
      <span className="text-sm">{token.symbol}</span>
      <ChevronDownIcon className="w-6 h-6" />
    </button>
  );
}

export default TokenSwitch;
