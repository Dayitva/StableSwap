import React from 'react';


const balanceClass = `bg-gray-900 py-2 px-6 rounded-full flex items-center space-x-2`;

/**
 * @title Balances
 * @description Component to display the balance of user of a token.
 * @returns JSX
 */
function Balances({kusdAmount, usdTzAmount, lpAmount}) {
  return (
    <div className="bg-gray-800 p-4 rounded-md 
      text-gray-100 flex items-center justify-around">
      <div className={balanceClass}>
        <span className="">
          💦
        </span>
        <span>
          {lpAmount}
        </span>
      </div>
      <div className={balanceClass}>
        <img 
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png" 
          alt="KUSD" 
          className="w-4 h-4"
        />
        <span>
          {kusdAmount}
        </span>
      </div>
      <div className={balanceClass}>
        <img 
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://quipuswap.com/tokens/usdtz.png" 
          alt="KUSD" 
          className="w-4 h-4"
        />
        
        <span className="">
          {usdTzAmount}
        </span>
      </div>
    </div>
  );
}

export default Balances;