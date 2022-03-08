import SlippageBadge from "./SlippageBadge";
import SlippageInputBadge from "./SlippageInputBadge";

export default function TimeSlippageBar({
  durations,
  currentDuration,
  setCurrentDuration,
  time = false,
}) {
  return (
    <div className="mt-3">
      <div className="flex flex-col sm:flex-row items-start space-y-1 sm:space-y-0 sm:items-center sm:justify-between mt-4">
        <div>
          <h1 className="text-md font-semibold">Transaction Deadline</h1>
        </div>
        <div className="flex items-center justify-end space-x-2">
          {/* For selecting slippage tolerance. */}
          {durations.map((value, index) => (
            <SlippageBadge
              key={index}
              slippage={value}
              active={value === currentDuration}
              onClick={() => {
                setCurrentDuration(value);
              }}
              time={time}
            />
          ))}
          <SlippageInputBadge
            slippage={currentDuration}
            // onClick={(e) => setCurrentDuration(e.target.value)}
            onChange={(e) => {
              setCurrentDuration((old) =>
                e.target.value < 30 ? e.target.value : old
              );
            }}
            time={time}
            active={!durations.includes(currentDuration)}
          />
        </div>
      </div>
    </div>
  );
}
