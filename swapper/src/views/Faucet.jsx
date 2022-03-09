import { useContext } from "react";
import { toast } from "react-toastify";
import Button from "../components/forms/Button";
import Navbar from "../components/Navbar";
import { getTokens } from "../utils/wallet";
import { LoadingContext } from "../contexts/LoadingContext";
import { set } from "lodash";

function Faucet() {
  const { setShowLoading } = useContext(LoadingContext);
  const handleGetTokens = async () => {
    try {
      setShowLoading(true);
      const data = await getTokens();
      setShowLoading(false);
      if (data.success) {
        toast(`Successfully airdropped. :)`);
      } else {
        toast(`Error: ${data.error}`);
      }
    } catch (error) {
      setShowLoading(false);
      toast(`Error: ${error.message}`);
    }
  };

  return (
    <div className="px-4">
      <Navbar />
      <div className="pt-16 mt-20">
        {/* Main Content Goes Here... */}
        <div className="mx-auto max-w-xl relative">
          <div className="bg-gray-900 border-2 border-gray-700 hover:border-gray-600 transition p-4 rounded-md relative">
            <h1 className="text-xl font-medium mb-2">Get Test Tokens</h1>
            <p className="text-gray-300">
              You can get our test kUSD & wUSDC tokens to try our platform. Just
              click on the button below and you'll get 1000 kUSD and 1000 wUSDC
              tokens. They ofc they don't have any real value associated with
              them.
            </p>
            <Button
              text="Get Tokens"
              bg="w-full text-lg bg-gradient-to-r from-purple-500 to-blue-500"
              padding="py-4 relative mt-5"
              onClick={handleGetTokens}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Faucet;
