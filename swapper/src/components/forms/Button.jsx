import React from "react";

function Button({ text, bg, padding, onClick, fontWeight }) {
  return (
    <div>
      <button
        className={`
          ${padding || "px-6 py-2"} text-xs font-${fontWeight || "regular"}} 
          rounded-sm text-white transition ${bg}`}
        onClick={onClick}
      >
        <span>{text}</span>
      </button>
    </div>
  );
}

export default Button;
