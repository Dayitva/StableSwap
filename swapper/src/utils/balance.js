import axios from "axios";

export const fetchMaxBalanceFA12 = async (userAddress, bigmapId) => {
  console.log(userAddress);
  let addr = userAddress.pkh;

  const url = `https://api.hangzhounet.tzkt.io/v1/bigmaps/${bigmapId}/keys?limit=10000`;
  const { data } = await axios.get(url);
  const userData = data.find((val) => val.key === addr);
  if (userData) {
    console.log("Before parseInt", userData.value.balance);
    return userData.value.balance;
  }
  return "0";
};

export const fetchMaxBalanceFA2 = async (userAddress, bigmapId, tokenId) => {
  console.log(userAddress);
  let addr = userAddress.pkh;

  const url = `https://api.hangzhounet.tzkt.io/v1/bigmaps/${bigmapId}/keys?limit=10000`;
  const { data } = await axios.get(url);
  const userData = data.find(
    (val) => val.key.address === addr && val.key.nat === tokenId.toString()
  );
  if (userData) {
    return userData.value;
  }
  return "0";
};
