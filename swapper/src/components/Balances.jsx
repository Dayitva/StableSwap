import React from "react";

const balanceClass = `bg-gray-900 py-2 px-6 rounded-full flex items-center space-x-2`;

function Balances({ kusdAmount, usdTzAmount, lpAmount, children }) {
  return (
    <div
      className="bg-gray-800 p-4 rounded-md 
      text-gray-100 flex items-center justify-around"
    >
      <span className="text-gray-500 text-xs font-medium absolute top-2 left-2">
        Wallet Balances
      </span>
      <br />
      <br />
      <br />
      <div className={balanceClass}>
        <span className="">💦</span>
        <span>
          {Number(parseFloat(lpAmount / 10 ** 9).toFixed(2)).toLocaleString()}
        </span>
      </div>
      <div className={balanceClass}>
        <img
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png"
          alt="KUSD"
          className="w-4 h-4"
        />
        <span>
          {Number(parseFloat(kusdAmount / 10 ** 9).toFixed(2)).toLocaleString()}
        </span>
      </div>
      <div className={balanceClass}>
        <img
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://quipuswap.com/tokens/usdtz.png"
          alt="KUSD"
          className="w-4 h-4"
        />

        <span className="">
          {Number(
            parseFloat(usdTzAmount / 10 ** 9).toFixed(2)
          ).toLocaleString()}
        </span>
      </div>
    </div>
  );
}

export default Balances;
