import React, { useEffect, useState } from "react";
import CONFIG from "../config";
import axios from "axios";

const balanceClass = `bg-gray-800 mt-2 py-2 px-6 rounded-full flex items-center space-x-2`;

function PoolStats() {
  const [tokenPool, setTokenPool] = useState(null);

  async function fetchTokenPool() {
    const { data } = await axios.get(
      `https://api.hangzhounet.tzkt.io/v1/contracts/${CONFIG.StableSwapAddress}/storage`
    );
    setTokenPool(data);
    // console.log(data)
  }

  useEffect(() => {
    setInterval(() => {
      fetchTokenPool();
    }, 30000);
    fetchTokenPool();
  }, []);

  return (
    <div className="bg-gray-900 p-4 rounded-md text-gray-100 border-2 border-gray-700">
      <p className="font-lg border-b border-gray-700 pb-3 mb-2">Pool Stats</p>
      <div className="flex items-center justify-around relative">
        <div className={balanceClass}>
          <img
            src="https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png"
            alt="KUSD"
            className="w-4 h-4"
          />
          <span>
            {Number(
              parseFloat(
                parseInt(tokenPool?.token_pool[0].pool) / 10 ** 18
              ).toFixed(2)
            ).toLocaleString()}
          </span>
        </div>
        <div className={balanceClass}>
          <img
            src="https://cloudflare-ipfs.com/ipfs/QmQfHU9mYLRDU4yh2ihm3zrvVFxDrLPiXNYtMovUQE2S2t"
            alt="wUSDC"
            className="w-4 h-4"
          />

          <span className="">
            {Number(
              parseFloat(
                parseInt(tokenPool?.token_pool[1].pool) / 10 ** 18
              ).toFixed(2)
            ).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  );
}

export default PoolStats;
