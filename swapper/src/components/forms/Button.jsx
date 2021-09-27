import React from "react";


function Button({text, bg, padding, onClick}) {
  return (
    <div>
      <button
        className={`
          ${padding || 'px-6 py-2'} text-sm font-semibold 
          rounded-sm text-white transition ${bg}`}
        onClick= {onClick}
      >
        <span>{text}</span>
      </button>
    </div>
  );
}

export default Button;
