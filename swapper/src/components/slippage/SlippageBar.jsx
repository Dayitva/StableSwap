import SlippageBadge from "./SlippageBadge";
import SlippageInputBadge from "./SlippageInputBadge";

export default function SlippageBar({
  slippages,
  currentSlippage,
  setCurrentSlippage,
}) {
  return (
    <div className="mt-3">
      <div className="flex items-center justify-between mt-4">
        <div>
          <h1 className="text-md ml-2">Slippage</h1>
        </div>
        <div className="flex items-center justify-end space-x-2">
          {/* For selecting slippage tolerance. */}
          {slippages.map((slippage, index) => (
            <SlippageBadge
              key={index}
              slippage={slippage}
              active={slippage === currentSlippage}
              onClick={() => {
                setCurrentSlippage(slippage);
              }}
            />
          ))}
          <SlippageInputBadge
            slippage={currentSlippage}
            // onClick={(e) => setCurrentSlippage(e.target.value)}
            onChange={(e) => {
              setCurrentSlippage((old) =>
                e.target.value < 30 ? e.target.value : old
              );
            }}
            active={!slippages.includes(currentSlippage)}
          />
        </div>
      </div>
    </div>
  );
}
