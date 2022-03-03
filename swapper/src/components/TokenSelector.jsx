import React, { useContext, useEffect } from "react";
import { XIcon } from "@heroicons/react/solid";
import { TokenListContext } from "../contexts/TokenListContext";
import config from "../config";
let tokenList = config.tokens;

function TokenSelector() {
  const { setShow, show, setToken, which, fromToken } =
    useContext(TokenListContext);
  useEffect(() => {
    console.log(`Token ${which}`);
    tokenList = config.tokens;

    if (which === "from") {
      tokenList = tokenList.filter((token) => token.id !== fromToken.id);
    }
  }, [which, fromToken.id]);
  return (
    <div
      className="w-[30rem] bg-gray-900 rounded-md shadow-2xl border-2 border-gray-600"
      style={{ width: "30rem" }}
    >
      <div className="p-3 flex items-center justify-between border-b border-gray-700">
        <h2 className="text-xl">Select a token</h2>
        <button
          onClick={() => {
            setShow(!show);
          }}
        >
          <XIcon className="w-4 h-4 hover:text-gray-300" />
        </button>
      </div>
      <div className="">
        {tokenList.map((token) => {
          return (
            // Render a component here.
            <div
              key={token.id}
              className="flex items-center px-6 py-4 hover:bg-gray-800 cursor-pointer transition"
              onClick={() => {
                setToken(token);
              }}
            >
              <img
                src={token.imageUrl}
                alt={token.name}
                className="w-9 h-9 rounded-full"
              />
              <div className="flex-1 ml-4 cursor-pointer flex justify-between items-center">
                <div>
                  <h1 className="text-lg font-medium">{token.symbol}</h1>
                  <p className="text-sm text-gray-400">{token.name}</p>
                </div>
                <span className="bg-purple-600 px-5 py-1.5 rounded-full text-xs font-semibold tracking-wide">
                  FA2
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default TokenSelector;
