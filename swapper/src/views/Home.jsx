import React from "react";
import DemoImage from "../assets/demo.png";
import SwapImage from "../assets/swap.png";
import TeamMemberDayitva from "../assets/dayitva.jpg";
import TeamMemberVivek from "../assets/vivek.png";
import TeamMemberDev from "../assets/dev.jpeg";
import Button from "../components/forms/Button";
import FeatureCard from "../components/FeatureCard";
import TeamCard from "../components/TeamCard";
import {
  CurrencyDollarIcon,
  RefreshIcon,
  UserGroupIcon,
} from "@heroicons/react/outline";
import Footer from "../Footer";

function Home() {
  return (
    <div>
      <div className="container mx-auto">
        {/* Main hero section div. */}
        <div
          className="flex items-center 
        justify-between py-10 flex-col md:flex-row mx-auto max-w-4xl pt-28"
        >
          <div className="flex-1 order-2 md:order-1 mt-20 md:mt-0">
            <h1 className="text-6xl font-semibold mb-2">Liquibrium</h1>
            <p className="text-xl leading-8 max-w-lg">
              Liquibrium is a decentralized exchange for tezos ecosystem which
              focuses on stable assets and provides the most optimum exchange
              value.
            </p>
            <div className="flex items-center space-x-4 mt-7">
              <Button
                text="Enter App"
                bg="bg-gradient-to-r from-purple-500 to-blue-500"
              />
              <Button text="Read Docs" bg="bg-gray-700" />
            </div>
          </div>
          <div className="order-1 md:order-2">
            <img src={DemoImage} alt="Liquibrium" />
          </div>
        </div>
      </div>

      {/* Main project feature cards component list. */}
      <div
        className="flex items-center justify-center space-x-0 
      space-y-10 md:space-y-0 py-40 my-4 flex-col lg:flex-row lg:space-x-4"
      >
        <FeatureCard
          title="Exchange Tokens"
          text="Exchange stablecoins at the lowest slippage"
        >
          <RefreshIcon className="w-6 h-6" />
        </FeatureCard>
        <FeatureCard
          title="Invest Liquidity"
          text="Get LP tokens for investing liquidity and earn fees"
        >
          <CurrencyDollarIcon className="w-6 h-6" />
        </FeatureCard>
        <FeatureCard
          title="DAO Governance"
          text="Be a part of the DAO &amp; govern key decisions"
        >
          <UserGroupIcon className="w-6 h-6" />
        </FeatureCard>
      </div>

      <div className="py-10 bg-gray-800">
        <h2 className="text-2xl font-semibold text-center">
          "Not every DEX is made for stable assets, Liquibrium is."
        </h2>
        <img className="mx-auto mt-10 h-20" src={SwapImage} alt="Swap" />
      </div>

      <div className=" py-40 my-4 ">
        <h1 className="text-center text-3xl font-semibold mb-7">Our Team</h1>
        <div
          className="flex items-center justify-center space-x-0 
      space-y-10 md:space-y-0 flex-col lg:flex-row lg:space-x-4"
        >
          <TeamCard
            imgSrc={TeamMemberDayitva}
            imgAlt="Dayitva Goel"
            twitterUsername="Dayitva_Goel"
          />
          <TeamCard
            imgSrc={TeamMemberVivek}
            imgAlt="Vivek Kumar"
            twitterUsername="vivekascoder"
          />
          <TeamCard
            imgSrc={TeamMemberDev}
            imgAlt="Dev Churiwala"
            twitterUsername="ChuriwalaDev"
          />
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default Home;
