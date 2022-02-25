export default function SlippageBadge({ slippage, active, onClick, ...props }) {
  return (
    <button
      className={`bg-purple-600 rounded-full px-3 py-1 text-xs font-semibold cursor-pointer hover:bg-purple-700 trasition ${
        active ? "ring-4 ring-purple-500 ring-opacity-30" : ""
      }`}
      onClick={onClick}
    >
      {slippage}%
    </button>
  );
}
