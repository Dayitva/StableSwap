import { MichelsonMap, TezosToolkit } from "@taquito/taquito";
import { BeaconWallet } from "@taquito/beacon-wallet";
import config from "../config";
// import { OpKind } from "@taquito/taquito";

const preferredNetwork = config.network;
const options = {
  name: "NFT",
  iconUrl: "https://tezostaquito.io/img/favicon.png",
  preferredNetwork: preferredNetwork,
};
const rpcURL = config.rpcUrl;
const wallet = new BeaconWallet(options);

const getActiveAccount = async () => {
  return await wallet.client.getActiveAccount();
};

const connectWallet = async () => {
  const wallet = new BeaconWallet(options);

  let account = await wallet.client.getActiveAccount();
  console.log("Hello Connecting wallet.");

  if (!account) {
    await wallet.requestPermissions({
      network: { type: preferredNetwork },
    });
    account = await wallet.client.getActiveAccount();
  }
  return { success: true, wallet: account.address };
};

const disconnectWallet = async () => {
  const wallet = new BeaconWallet(options);

  await wallet.disconnect();
  return { success: true, wallet: null };
};

const checkIfWalletConnected = async (wallet) => {
  try {
    const activeAccount = await wallet.client.getActiveAccount();
    if (!activeAccount) {
      await connectWallet();
    }

    return {
      success: true,
    };
  } catch (error) {
    return {
      success: false,
      error,
    };
  }
};

export const changeName = async (name) => {
  const wallet = new BeaconWallet(options);
  const response = await checkIfWalletConnected(wallet);

  if (response.success) {
    const tezos = new TezosToolkit(rpcURL);
    tezos.setWalletProvider(wallet);
    const contract = await tezos.wallet.at(config.contractAddress);
    const operation = await contract.methods.default(name).send();
    const result = await operation.confirmation();
    console.log(result);
  }
};

export const exchange = async (fromToken, amount, minReturn, validUpto) => {
  const wallet = new BeaconWallet(options);
  const response = await checkIfWalletConnected(wallet);
  if (response.success) {
    const tezos = new TezosToolkit(rpcURL);
    tezos.setWalletProvider(wallet);
    const pkh = await tezos.wallet.pkh();
    console.log(fromToken, pkh, fromToken.address, config.StableSwapAddress);

    const fromTokenContract = await tezos.wallet.at(fromToken.address);
    const dexContract = await tezos.wallet.at(config.StableSwapAddress);

    const batch = await tezos.wallet
      .batch()
      .withContractCall(
        fromToken.isFA2
          ? fromTokenContract.methods.update_operators([
              {
                add_operator: {
                  owner: pkh,
                  operator: config.StableSwapAddress,
                  token_id: fromToken.id,
                },
              },
            ])
          : fromTokenContract.methods.approve(config.StableSwapAddress, amount)
      )
      .withContractCall(
        dexContract.methods.exchange(
          amount,
          fromToken.tokenId,
          minReturn,
          validUpto
        )
      );
    const op = await batch.send();
    await op.confirmation();
    return {
      success: true,
      hash: op.opHash,
    };
  } else {
    return {
      success: false,
    };
  }
};

export const removeLiquidity = async (amount, min_0, min_1) => {
  const wallet = new BeaconWallet(options);
  const response = await checkIfWalletConnected(wallet);
  if (response.success) {
    const tezos = new TezosToolkit(rpcURL);
    tezos.setWalletProvider(wallet);

    const dexContract = await tezos.wallet.at(config.StableSwapAddress);

    const batch = await tezos.wallet.batch().withContractCall(
      dexContract.methods.remove_liquidity(
        amount,
        MichelsonMap.fromLiteral({
          0: min_0,
          1: min_1,
        })
      )
    );
    const op = await batch.send();
    await op.confirmation();
    return {
      success: true,
      hash: op.opHash,
    };
  } else {
    return {
      success: false,
    };
  }
};

export const addLiquidity = async (fromToken, amount, minReturn, validUpto) => {
  const wallet = new BeaconWallet(options);
  const response = await checkIfWalletConnected(wallet);
  if (response.success) {
    const tezos = new TezosToolkit(rpcURL);
    tezos.setWalletProvider(wallet);
    const pkh = await tezos.wallet.pkh();
    console.log(fromToken, pkh, fromToken.address, config.StableSwapAddress);

    const fromTokenContract = await tezos.wallet.at(fromToken.address);
    const dexContract = await tezos.wallet.at(config.StableSwapAddress);

    const batch = await tezos.wallet
      .batch()
      .withContractCall(
        fromToken.isFA2
          ? fromTokenContract.methods.update_operators([
              {
                add_operator: {
                  owner: pkh,
                  operator: config.StableSwapAddress,
                  token_id: fromToken.id,
                },
              },
            ])
          : fromTokenContract.methods.approve(config.StableSwapAddress, amount)
      )
      .withContractCall(
        fromToken.tokenId === 0
          ? dexContract.methods.add_liquidity(amount, 0, 1)
          : dexContract.methods.add_liquidity(0, amount, 1)
      );
    const op = await batch.send();
    await op.confirmation();
    return {
      success: true,
      hash: op.opHash,
    };
  } else {
    return {
      success: false,
    };
  }
};

export const getTokens = async () => {
  const wallet = new BeaconWallet(options);
  const response = await checkIfWalletConnected(wallet);
  if (response.success) {
    const tezos = new TezosToolkit(rpcURL);
    tezos.setWalletProvider(wallet);
    const kusd = await tezos.wallet.at(config.tokens[0].address);
    const wusdc = await tezos.wallet.at(config.tokens[1].address);

    const batch = await tezos.wallet
      .batch()
      .withContractCall(kusd.methods.mint_tokens())
      .withContractCall(wusdc.methods.mint_tokens(config.tokens[1].tokenId));
    const op = await batch.send();
    await op.confirmation();
    return {
      success: true,
      hash: op.opHash,
    };
  } else {
    return {
      success: false,
    };
  }
};

// export const fetchSaleStat = async () => {
//   const tezos = new TezosToolkit(rpcURL);
//   const contract = await tezos.contract.at(config.contractAddress);
//   const storage = await contract.storage();
//   const maxSupply = storage.maxSupply;
//   const totalMinted = storage.nMinted;
//   return {
//     maxSupply: maxSupply.toNumber(),
//     totalMinted: totalMinted.toNumber(),
//   };
// };

export {
  connectWallet,
  disconnectWallet,
  getActiveAccount,
  checkIfWalletConnected,
};
