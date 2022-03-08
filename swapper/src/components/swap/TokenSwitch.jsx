import React from "react";
import { ChevronDownIcon } from "@heroicons/react/solid";

function TokenSwitch({ click, token }) {
  return (
    <button
      className="flex items-center space-x-1 bg-gray-900 hover:bg-gray-700 px-2 py-1 rounded-full focus:outline-none transition"
      onClick={click}
    >
      <img
        src={token.imageUrl}
        className="sm:w-6 sm:h-6 w-4 h-4"
        alt={token.symbol}
      />
      <span className="text-xs font-semibold sm:font-normal sm:text-sm">
        {token.symbol}
      </span>
      <ChevronDownIcon className="sm:w-6 sm:h-6 w-4 h-4" />
    </button>
  );
}

export default TokenSwitch;
