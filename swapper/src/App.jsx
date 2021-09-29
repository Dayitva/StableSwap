import React, { useContext } from "react";
import Error from "./components/error/Error";
import Navbar from "./components/Navbar";
import Swap from "./components/Swap";
import TokenSelector from "./components/TokenSelector";
import { TokenListContext } from "./contexts/TokenListContext";

function App() {
  const { show } = useContext(TokenListContext);
  return (
    <div className="min-h-screen bg-dark relative text-white">
      <Navbar />
      {show ? (
        <div className="absolute inset-0 bg-black z-50 bg-opacity-40 flex items-start pt-36 justify-center">
          <TokenSelector />
        </div>
      ) : (
        ""
      )}
      <div className="pt-16">
        {/* Main Content Goes Here... */}
        <div className="mt-20 mx-auto max-w-2xl relative">
          {/* Wrapper for swap component... */}
          <div className="absolute -inset-0.5 bg-gray-800 blur"></div>
          <Swap />
        </div>
      </div>
      <Error />
    </div>
  );
}

export default App;
