import React, { useContext, useEffect } from "react";
import { XIcon } from "@heroicons/react/solid";
import { TokenListContext } from "../contexts/TokenListContext";
import config from "../config";

function TokenSelector() {
  const { setShow, show, setToken, which, fromToken, list, setList } =
    useContext(TokenListContext);

  useEffect(() => {
    console.log(`Token ${which}`);
    setList(config.tokens);

    if (which === "to") {
      setList((list) => list.filter((token) => token.id !== fromToken.id));
    }
  }, [which]);

  return (
    <div
      className="w-[30rem] bg-gray-900 rounded-md shadow-2xl border-2 border-gray-600 mx-2"
      style={{ width: "30rem" }}
    >
      <div className="p-3 flex items-center justify-between border-b border-gray-700">
        <h2 className="sm:text-xl text-md font-semibold">Select a token</h2>
        <button
          onClick={() => {
            setShow(!show);
          }}
        >
          <XIcon className="w-4 h-4 hover:text-gray-300" />
        </button>
      </div>
      <div className="">
        {list.map((token) => {
          return (
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
                  <h1 className="text-base sm:text-lg font-medium">
                    {token.symbol}
                  </h1>
                  <p className="text-xs sm:text-sm text-gray-400">
                    {token.name}
                  </p>
                </div>
                <span className="bg-purple-600 px-4 sm:px-5 py-1 sm:py-1.5 rounded-full text-xxs sm:text-xs font-semibold tracking-wide">
                  {token.isFA2 ? "FA2" : "FA1.2"}
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
