import SlippageBadge from "./SlippageBadge";
import SlippageInputBadge from "./SlippageInputBadge";

export default function SlippageBar({
  slippages,
  currentSlippage,
  setCurrentSlippage,
}) {
  return (
    <div className="mt-3">
      <div className="flex flex-col sm:flex-row items-start space-y-1 sm:space-y-0 sm:items-center sm:justify-between mt-4">
        <div>
          <h1 className="font-semibold text-md">Slippage</h1>
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
