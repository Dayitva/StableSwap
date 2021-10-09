import React from "react";
import Button from "./forms/Button";

function FeatureCard({ title, children }) {
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
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Mollitia,
            totam aut magni earum voluptatibus neque debitis quaerat nihil
            excepturi? Voluptatum placeat praesentium delectus nam obcaecati
            velit sed magnam quos,
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
