import React from "react";
import TokenSwitch from "./TokenSwitch";
// import {TokenListContext} from '../../contexts/TokenListContext';

function InputBox({ onTokenSwitchClick, token, value, setValue }) {
  // onTokenSwitchClick: When you click on the tokenSwitch Button.
  // const {show, setShow} = useContext(TokenListContext);
  return (
    <div className="bg-gray-800  rounded-sm border-gray-700 relative">
      <div className="absolute top-2 left-3">
        <TokenSwitch click={onTokenSwitchClick} token={token} />
      </div>
      <input
        type="number"
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
        }}
        className="w-full bg-transparent text-2xl font-semibold px-3 py-6 text-right focus:outline-none border-2 rounded-md border-gray-800 hover:border-gray-700 transition"
      />
    </div>
  );
}

export default InputBox;
