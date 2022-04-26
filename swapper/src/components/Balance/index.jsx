import BigNumber from "bignumber.js";
import { useEffect, useState } from "react";
import config from "../../config";
import { fetchMaxBalanceFA12, fetchMaxBalanceFA2 } from "../../utils/balance";
import { getUserAddress } from "../../utils/wallet";

const tokens = [
  {
    name: "kUSD",
    fa2: false,
    bigmapId: config.tokens[0].balanceBigmap,
    decimals: config.tokens[0].decimals,
    tokenId: 0,
  },
  {
    name: "USDtz",
    fa2: true,
    bigmapId: config.tokens[1].balanceBigmap,
    decimals: config.tokens[1].decimals,
    tokenId: 0,
  },
  {
    name: "LLP",
    fa2: false,
    bigmapId: config.lpToken.balanceBigmap,
    decimals: config.lpToken.decimals,
    tokenId: 0,
  },
];

export default function Balance() {
  const [balances, setBalances] = useState([]);

  const fetchUserBalances = async (tokens) => {
    const userAddress = await getUserAddress();
    const balances = [];
    for (let i = 0; i < tokens.length; i++) {
      const token = tokens[i];
      let balance = "0";
      if (token.fa2) {
        balance = await fetchMaxBalanceFA2(
          userAddress,
          token.bigmapId,
          token.tokenId
        );
      } else {
        balance = await fetchMaxBalanceFA12(userAddress, token.bigmapId);
      }
      console.log(token.name, balance);
      balances.push({
        name: token.name,
        balance: new BigNumber(balance)
          .dividedBy(10 ** token.decimals)
          .toFixed(2),
      });
    }
    return balances;
  };

  useEffect(() => {
    const fetchData = async () => {
      setBalances(await fetchUserBalances(tokens));
      console.log(balances);
    };
    fetchData();
    setInterval(() => {
      fetchData();
    }, 20000);
  }, []);

  return (
    <div className="flex space-x-4">
      <div className="flex items-center justify-center bg-gray-900 rounded-md border-2 border-gray-600">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-white m-10"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"
          />
        </svg>
      </div>
      <div className="flex-1 bg-gray-900 rounded-md border-2 border-gray-600 py-3 px-5">
        <h2 className="font-semibold border-b border-gray-600 pb-2 mb-4">
          Your Balance
        </h2>
        <div className="mt-2 flex items-center justify-around">
          {balances.map((balance, index) => (
            <p className="text-xs" key={index}>
              <span className="font-semibold">{balance.name}:</span>{" "}
              {balance.balance}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}
