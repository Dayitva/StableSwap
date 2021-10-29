import axios from "axios";
import { useContext, useState } from "react";
import { LoadingContext } from "../contexts/LoadingContext";
import { ErrorContext } from "../contexts/ErrorContext";

function Faucet() {
  const {setShowLoading} = useContext(LoadingContext);
  const { showMessage } = useContext(ErrorContext);

  const [address, setAddress] = useState("");
  const giveMeSome = async (tokenName) => {
    setShowLoading(true);
    if (!address) {
      showMessage("Not a valid address.")
      return
    }
    try {
      const {data} = await axios.post('https://faucet.divcorn.com/mint', {
        address: address,
        tokenName: tokenName
      })
      console.log(data) 
      showMessage(data.opHash);
      setShowLoading(false); 
    } catch (error) {
      console.log(error)
      setShowLoading(false);
    }
  }
  return (
    <div className="pt-20 container mx-auto px-4">
      <h1 className="text-white font-semibold text-xl">
        Liquibrium's Faucet
      </h1>
      <div className="mt-4"> 
        <p className="mb-2">Enter your address:</p>
        <input type="text" className="bg-gray-800 text-white w-full" value={address} onChange={(e) => {setAddress(e.target.value)}}/>
        <button 
          className="text-xs uppercase font-semibold px-6 py-2 bg-green-500 mt-2"
          onClick={() => giveMeSome("usdtz")}
        >Get USDtz</button>
        <button 
          className="text-xs uppercase font-semibold px-6 py-2 bg-blue-500 mt-2 ml-3"
          onClick={() => giveMeSome("kusd")}
        >Get KUSD</button>
      </div>
    </div>
  );
}

export default Faucet;