export default function SlippageInputBadge({
  slippage,
  onClick,
  onChange,
  active,
}) {
  return (
    <span className="relative">
      <input
        type={"number"}
        className={`w-16 bg-purple-600 rounded-full px-3 py-1 text-xs font-semibold cursor-pointer hover:bg-purple-700 focus:outline-none trasition 
          focus:ring-4 focus:ring-purple-500 focus:ring-opacity-30
        `}
        onClick={onClick}
        placeholder={slippage}
        onChange={onChange}
      />
      <span className="absolute right-2 top-1/2 transform text-xs -translate-y-1/2 ">
        %
      </span>
    </span>
  );
}
