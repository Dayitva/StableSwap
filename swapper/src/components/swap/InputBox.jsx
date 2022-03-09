import React from "react";
import TokenSwitch from "./TokenSwitch";
import Button from "../forms/Button";

function InputBox({ onTokenSwitchClick, token, value, setValue }) {
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
        className="w-full bg-transparent text-xl sm:text-2xl font-semibold px-3 sm:py-5 py-3 text-right focus:outline-none border-2 rounded-md border-gray-800 hover:border-gray-700 transition"
      />
      {/* <div className="absolute bottom-2 left-3">
        <Button 
        text="Max"
        bg="rounded-full sm:text-lg text-xs font-semibold bg-gradient-to-r from-purple-500 to-blue-500"/>
      </div> */}
    </div>
  );
}

export default InputBox;
