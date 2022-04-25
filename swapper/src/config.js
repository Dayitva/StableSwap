const config = {
  KusdAddress: "KT1WJUr74D5bkiQM2RE1PALV7R8MUzzmDzQ9",
  kusdBigmapId: 65911,
  UsdtzAddress: "KT1CNQL6xRn5JaTUcMmxwSc5YQjwpyHkDR5r",
  usdtzBigmapId: 65914,
  StableSwapAddress: "KT1GmHh4kpH7wVedjpHLGRcMWtUJUF9pMLMT",
  lpBigmapId: 89965,

  // Config parameters that are used.
  // Testnet config.
  // network: "hangzhounet",
  // preferredNetwork: "hangzhounet",
  // rpcUrl: "https://hangzhounet.smartpy.io",

  // Mainnet config.
  network: "mainnet",
  preferredNetwork: "mainnet",
  rpcUrl: "https://mainnet.smartpy.io",

  // Some contract info to rerduce time for API calls.
  fee: 0.15,
  tokens: [
    {
      id: 1,
      symbol: "kUSD",
      address: "KT1K9gCRgaLRFKTErYt1wVxA3Frb9FjasjTV",
      name: "Kolibri USD",
      imageUrl:
        "https://img.templewallet.com/insecure/fit/64/64/ce/0/plain/https://kolibri-data.s3.amazonaws.com/logo.png",
      tokenId: 0,
      decimals: 18,
      isFA2: false,
      balanceBigmap: 380,
    },
    {
      id: 2,
      symbol: "USDtz",
      address: "KT1LN4LPSqTMS7Sd2CJw4bbDGRkMv2t68Fy9",
      name: "USDtez",
      imageUrl:
        "https://cloudflare-ipfs.com/ipfs/Qmb2GiHN9EjcrN29J6y9PsXu3ZDosXTv6uLUWGZfRRSzS2/usdtz.png",
      tokenId: 0,
      decimals: 6,
      isFA2: false,
      balanceBigmap: 36,
    },
  ],
  lpToken: {
    symbol: "LLP",
    address: "KT1UzZVdbPLk5U3w6hVei1Z715YvMLPFfmfk",
    isFA2: false,
    balanceBigmap: 153251,
    decimals: 18,
  },
};

export default config;
