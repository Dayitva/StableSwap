import { useState } from "react";
import AddLiquidity from "../AddLiquidity";
import RemoveLiquidity from "../RemoveLiquidity";

export default function LiquidityTab() {
  const tabs = [
    { title: "Add Liquidity", component: <AddLiquidity /> },
    { title: "Remove Liquidity", component: <RemoveLiquidity /> },
  ];
  const [selected, setSelected] = useState(tabs[0]);

  return (
    <div className="bg-gray-900 border-2 border-gray-700 p-4 rounded-md relative">
      <div className="flex items-center space-x-4 mb-4 border-b-2 border-gray-800">
        {tabs.map((tab, index) => (
          <span key={index} onClick={() => setSelected(tab)} className={`cursor-pointer border-b-2 pb-2 border-transparent hover:border-b-2 hover:border-white hover:text-white transition-all text-md font-medium ${selected.title === tab.title ? 'border-white text-white': 'text-gray-400'}`}>
            {tab.title}
          </span>
        ))}
      </div>
      <div>{selected.component}</div>
    </div>
  );
}
