import React from "react";
import Button from "../components/forms/Button";
import ReactTooltip from "react-tooltip";

function Home() {

  const redirectToApp = async () => {
    window.location.href = "https://testnet.liquibrium.finance/exchange";
  };

  const showDocs = async () => {
    alert("Coming Soon");
  }

  return (
    <div className="pb-20">
      <ReactTooltip />
      <div className="container mx-auto">
        {/* Main hero section div. */}
        <div
          className="flex items-center 
        justify-between py-10 flex-col md:flex-row mx-auto max-w-4xl pt-10 px-4"
        >
          <div className="flex-1 order-2 md:order-1 mt-20 md:mt-0">
            <h1 className="text-5xl sm:text-6xl font-semibold mb-2">
              Liquibrium
            </h1>
            <p className="text-md sm:text-xl sm:leading-8 max-w-lg">
              Liquibrium is a decentralized exchange for the Tezos ecosystem which
              focuses on stable assets and provides the most optimum exchange
              value.
            </p>
            <div className="flex items-center space-x-4 mt-7">
              <Button
                text="Enter App"
                bg="bg-gradient-to-r from-purple-500 to-blue-500 py-3 font-semibold uppercase"
                onClick={redirectToApp}
              />
              <Button
                text="Read Docs"
                bg="bg-gray-700 py-3 font-semibold uppercase hover:bg-gray-800"
                onClick={showDocs}
              />
            </div>
          </div>
          <div className="order-1 md:order-2">
            <img
              src={"/assets/demo.png"}
              alt="Liquibrium"
              className="w-60 sm:w-96"
            />
          </div>
        </div>
      </div>
      <div className="p-4">
        <div
          className="flex items-center 
          justify-center py-10 flex-col mx-auto max-w-4xl"
        >
          <h1 className="text-4xl font-semibold mb-4">
            Our <span className="text-purple-600">Backers</span>
          </h1>
          <div className="flex items-center space-x-20">
            <a
              className="flex flex-col items-center justify-center"
              href="https://www.antler.co/"
              target={"_blank"}
            >
              <svg width="80px" height="80px" viewBox="0 0 54 54" role="img">
                <title>Antler</title>
                <path
                  fill="#fff"
                  fillRule="evenodd"
                  d="M37.17 42.215L26.904 18.144 16.65 42.214h-5.454l13.333-30.429h4.954l13.321 30.43H37.17zM0 54h54V0H0v54z"
                ></path>
              </svg>
              <p className="text-sm font-semibold mt-2">Antler</p>
            </a>
            <a
              className="flex flex-col items-center justify-center"
              href="https://tezos.foundation/"
              target={"_blank"}
            >
              <svg
                className="w-20 h-20"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1169.87 1593"
                datatip="Hello"
              >
                <title>tezos-logo-01</title>
                <g id="Layer_2">
                  <path
                    d="M755.68,1593q-170.51,0-248.91-82.14a253.6,253.6,0,0,1-78.15-177,117.39,117.39,0,0,1,13.69-58.5A101.21,101.21,0,0,1,479.64,1238a130.22,130.22,0,0,1,116.24,0A99.55,99.55,0,0,1,633,1275.36a115,115,0,0,1,14.18,58.5,111.73,111.73,0,0,1-19.91,68.45,92.78,92.78,0,0,1-47.31,34.62,129.18,129.18,0,0,0,74.67,46.55,370,370,0,0,0,101.8,14.68,226.91,226.91,0,0,0,128.19-38.33,224,224,0,0,0,83.63-113.25,492,492,0,0,0,27.38-169.5,465.07,465.07,0,0,0-29.87-176.23,217.54,217.54,0,0,0-86.37-109.52,229.68,229.68,0,0,0-124.43-35.59,236.75,236.75,0,0,0-107.78,36.59L567.26,932.4V892.33L926.43,410.5H428.62v500A178.9,178.9,0,0,0,456,1012.8a94.34,94.34,0,0,0,83.63,40.07,139.85,139.85,0,0,0,82.63-29.12,298.38,298.38,0,0,0,69.2-71.19,24.86,24.86,0,0,1,9-11.94,18.4,18.4,0,0,1,12-4.48,41.55,41.55,0,0,1,23.4,9.95,49.82,49.82,0,0,1,12.69,33.85,197.86,197.86,0,0,1-4.48,24.89,241,241,0,0,1-85.38,106,211.78,211.78,0,0,1-119.76,36.38q-161.67,0-224-63.72A238.67,238.67,0,0,1,253.2,909.25V410.5H0V317.6H254.38V105.78L196.14,47.5V0h169l63.48,32.86V317.6l657.6-2,65.47,65.71L748.46,786.5a271,271,0,0,1,76.16-18.42A330.1,330.1,0,0,1,972,810.15a302.7,302.7,0,0,1,126.95,113.29,399.78,399.78,0,0,1,57.25,136.65,575.65,575.65,0,0,1,13.69,117,489.39,489.39,0,0,1-49.78,216.79,317.92,317.92,0,0,1-149.35,149.35A483.27,483.27,0,0,1,755.68,1593Z"
                    style={{ fill: "#fff" }}
                    // style={{ fill: "#ED4747" }}
                  />
                </g>
              </svg>
              <p className="text-sm font-semibold mt-2">Tezos Foundation</p>
            </a>
          </div>
        </div>
      </div>

      <div className="bg-black p-7 absolute bottom-0 left-0 right-0 border-t-2 border-gray-900">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <p className="text-center text-sm font-semibold">
            &copy; 2022 Liquibrium
          </p>
          <ul className="flex space-x-4">
            <li>
              <a
                href="https://twitter.com/liquibrium"
                className="hover:text-purple-500 hover:underline text-sm"
              >
                Twitter
              </a>
            </li>
            <li>
              <a
                href="https://discord.gg/nNnsp4fxqx"
                className="hover:text-purple-500 hover:underline text-sm"
              >
                Discord
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Home;
