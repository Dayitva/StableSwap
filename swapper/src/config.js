const config = {
  KusdAddress: "KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9",
  kusdBigmapId: 65911,
  UsdtzAddress: "KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r",
  usdtzBigmapId: 65914,
  StableSwapAddress: "KT1CsExBNMY8Aa3H7BCpD6egUBYcYyVU5zp5",
  lpBigmapId: 89965,

  // Config parameters that are used.
  network: "hangzhounet",
  preferredNetwork: "hangzhounet",
  rpcUrl: "https://hangzhounet.smartpy.io",

  // Some contract info to rerduce time for API calls.
  fee: 0.15,
  tokens: [
    {
      id: 1,
      symbol: "kUSD",
      address: "KT1EMDNRdR2T4b3NEVRExmwc1WhhjbpmGMq2",
      name: "Kolibri USD",
      imageUrl:
        "https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png",
      tokenId: 0,
      decimals: 18,
      isFA2: false,
      balanceBigmap: 165890,
    },
    {
      id: 2,
      symbol: "wUSDC",
      address: "KT1Rbr1z6AC8FoHVs8cCMQwi8pLCzjUpFd2n",
      name: "Wrapped USDC",
      imageUrl:
        "https://cloudflare-ipfs.com/ipfs/QmQfHU9mYLRDU4yh2ihm3zrvVFxDrLPiXNYtMovUQE2S2t",
      tokenId: 1,
      decimals: 6,
      isFA2: true,
      balanceBigmap: 165968,
    },
  ],
  lpToken: {
    symbol: "LLP",
    address: "KT1TaynG42eaZEmSSsprWe16e6oTUH9yNJAo",
    isFA2: false,
    balanceBigmap: 233591,
    decimals: 18,
  },
};

export default config;
