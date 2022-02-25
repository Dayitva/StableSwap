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
      <div className="flex items-center justify-between">
        {tabs.map((tab, index) => (
          <span key={index} onClick={() => setSelected(tab)}>
            {tab.title}
          </span>
        ))}
      </div>
      <div>{selected.component}</div>
    </div>
  );
}
