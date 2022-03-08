export default function SlippageInputBadge({
  slippage,
  onClick,
  onChange,
  active,
  time,
}) {
  return (
    <span className="relative">
      <input
        type={"number"}
        className={`w-14 sm:w-16 bg-purple-600 rounded-full px-3 py-1 text-xxs sm:text-xs font-semibold cursor-pointer hover:bg-purple-700 focus:outline-none trasition 
          focus:ring-4 focus:ring-purple-500 focus:ring-opacity-30 ${
            active ? "ring-4 ring-purple-500 ring-opacity-30" : ""
          }
        `}
        onClick={onClick}
        placeholder={slippage}
        onChange={onChange}
        value={slippage}
      />
      <span className="absolute right-2 top-1/2 transform text-xs -translate-y-1/2 text-xxs sm:text-xs font-semibold">
        {time ? "m" : "%"}
      </span>
    </span>
  );
}
