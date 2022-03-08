import React from "react";

function PlainInputBox({ label, value, setValue, type }) {
  return (
    <div className="bg-gray-800  rounded-md border-gray-700 relative">
      <p className="text-gray-400 text-xs p-2 absolute top-0 left-0">
        {label}:{" "}
      </p>
      <input
        type={type}
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
        }}
        className="w-full bg-transparent text-xl sm:text-2xl font-semibold px-3 py-3 sm:py-6 text-right focus:outline-none"
      />
    </div>
  );
}

export default PlainInputBox;
