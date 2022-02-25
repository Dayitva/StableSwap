import React, { useContext } from "react";
import { XIcon } from "@heroicons/react/solid";
import { TokenListContext } from "../contexts/TokenListContext";
import { tokenList } from "../utils/tokenList";

function TokenSelector() {
  const { setShow, show, setToken } = useContext(TokenListContext);
  return (
    <div
      className="w-[30rem] bg-gray-900 rounded-md shadow-2xl"
      style={{ width: "30rem" }}
    >
      <div className="p-3 flex items-center justify-between border-b border-gray-700">
        <h2>Select a token</h2>
        <button
          onClick={() => {
            setShow(!show);
          }}
        >
          <XIcon className="w-4 h-4" />
        </button>
      </div>
      <div className="">
        {tokenList.map((token) => {
          return (
            // Render a component here.
            <div
              key={token.id}
              className="flex items-center px-6 py-4 hover:bg-gray-800 cursor-pointer"
              onClick={() => {
                setToken(token);
              }}
            >
              <img
                src={token.imageUrl}
                alt={token.name}
                className="w-9 h-9 rounded-full"
              />
              <div className="flex-1 ml-4 cursor-pointer">
                <h1 className="text-lg font-medium">{token.symbol}</h1>
                <p className="text-sm text-gray-400">{token.name}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default TokenSelector;
