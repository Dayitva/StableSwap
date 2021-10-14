import React, { useEffect, useState } from "react";
import CONFIG from "../config";
import axios from "axios";

const balanceClass = `bg-gray-900 py-2 px-6 rounded-full flex items-center space-x-2`;


function PoolStats() {
  const [tokenPool, setTokenPool] = useState(null);
  
  async function fetchTokenPool() {
    const {data} = await axios.get(
      `https://api.granadanet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    )
    setTokenPool(data);
    console.log(data)
  }

  useEffect(() => {  
    setInterval(() => {
      fetchTokenPool();
    }, 30000)
    fetchTokenPool();
  }, [])


  return (
    <div className="bg-gray-800 p-4 rounded-md 
      text-gray-100 flex items-center justify-around relative">
      <span className="text-gray-500 text-xs font-medium absolute top-2 left-2">Pool Stats</span>
      <div className={balanceClass}>
        <img 
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png" 
          alt="KUSD" 
          className="w-4 h-4"
        />
        <span>
          {parseFloat(parseInt(tokenPool?.token_pool[0].pool) / 10 ** 9).toFixed(2)}
        </span>
      </div>
      <div className={balanceClass}>
        <img 
          src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://quipuswap.com/tokens/usdtz.png" 
          alt="KUSD" 
          className="w-4 h-4"
        />
        
        <span className="">
          {parseFloat(parseInt(tokenPool?.token_pool[1].pool) / 10 ** 9).toFixed(2)}
        </span>
      </div>
    </div>
  );
}

export default PoolStats;