import { useState } from 'react';
import PlainInputBox from './PlainInputBox';
import Button from './forms/Button';

function RemoveLiquidity() {
  const [lpAmount, setLpAmount] = useState(0);
  function removeLiquidity() {

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