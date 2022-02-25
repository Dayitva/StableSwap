import { TezosToolkit } from "@taquito/taquito";
import { BeaconWallet } from "@taquito/beacon-wallet";
import config from "../config";
import { OpKind } from "@taquito/taquito";

const preferredNetwork = config.network;
const options = {
  name: "NFT",
  iconUrl: "https://tezostaquito.io/img/favicon.png",
  preferredNetwork: preferredNetwork,
};
const rpcURL = config.rpcURL;
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

// export const mintNFT = async (quantity) => {
//   const now = new Date();
//   const delta = now - config.publicSaleTime > 0;
//   // const delta = true;

//   const wallet = new BeaconWallet(options);
//   const response = await checkIfWalletConnected(wallet);
//   if (response.success) {
//     const tezos = new TezosToolkit(rpcURL);
//     tezos.setWalletProvider(wallet);

//     const contract = await tezos.wallet.at(config.contractAddress);

//     let microTransactions = [];
//     for (let i = 0; i < quantity; i++) {
//       microTransactions.push({
//         kind: OpKind.TRANSACTION,
//         ...contract.methods.mint(i).toTransferParams(),
//         amount: delta ? config.publicSalePrice : config.price,
//         mutez: false,
//       });
//     }

//     const batch = await tezos.wallet.batch(microTransactions);
//     const batchOp = await batch.send();
//     console.log("Operation hash:", batchOp);
//     let hash = batchOp.opHash;
//     await batchOp.confirmation();
//     return {
//       success: true,
//       hash: hash,
//     };
//   } else {
//     return {
//       success: false,
//     };
//   }
// };

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
