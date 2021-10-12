import { useState, useContext } from 'react';
import PlainInputBox from './PlainInputBox';
import Button from './forms/Button';
import { ErrorContext } from "../contexts/ErrorContext";
import { TezosContext } from '../contexts/TezosContext';
import CONFIG from '../config';

function RemoveLiquidity() {
  const [lpAmount, setLpAmount] = useState(0);
  const { showMessage } = useContext(ErrorContext);
  const {tezos} = useContext(TezosContext);

  async function removeLiquidity() {
    const stableSwapContract = await tezos.wallet.at(CONFIG.StableSwapAddress);
    const amount = parseInt(lpAmount * 10 ** 9);
    const op = await stableSwapContract.methods.remove_liquidity(amount).send();
    showMessage(`✅ ${op.opHash}`)
    const result = op.confirmation();
    console.log(result);
  }

  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center justify-between">
        <h1>Remove Liquidity</h1>
      </div>
      <div className="space-y-4 mt-2">
        <PlainInputBox
          label={"Amount of Lp"}
          value={lpAmount}
          setValue={setLpAmount}
        />
      </div>

      <div className="mt-4">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur"></div>
          <Button
            text="Remove Liquidity"
            bg="w-full bg-blue-500"
            padding="py-4 relative"
            onClick={removeLiquidity}
          />
        </div>
      </div>
    </div>
  );
}

export default RemoveLiquidity;