import React from "react";
import Button from "./forms/Button";

function FeatureCard({ title, text, children }) {
  return (
    <div>
      <div className="p-7 bg-gray-800 rounded-md w-96">
        <div className="flex items-center justify-center space-x-3 mb-8">
          <span className="bg-gray-700 p-2 rounded-md">
            {/* <x className="w-6 h-6" /> */}
            {children}
          </span>
          <p className="text-xl font-semibold">{title}</p>
        </div>
        <div>
          <p className="text-sm leading-6 text-center">
            {text}
          </p>
        </div>
        <div className="mt-8">
          <Button
            text="Learn More"
            bg="bg-gradient-to-r from-purple-500 to-blue-500 w-full"
          />
        </div>
      </div>
    </div>
  );
}

export default FeatureCard;
