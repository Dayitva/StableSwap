import { compose } from '@taquito/taquito'
import {Tzip12Module, tzip12} from '@taquito/tzip12'
import {tzip16} from '@taquito/tzip16';

async function getDecimals(tezos, tokenAddress) {
  /* Returns the no of decimals in a FA1.2 contract from the tokenAddress */
  console.log(tokenAddress)
  tezos.addExtension(new Tzip12Module());
  const contract = await tezos.contract.at(tokenAddress, compose(tzip12, tzip16));
  const metadata = await contract.tzip16().getTokenMetadata(0);
  return metadata;
}

export {getDecimals};