import React from "react";
import Button from './forms/Button';

function Navbar() {
  return (
    <div className="fixed left-0 right-0 top-0 h-16 shadow-md border-b-2 border-gray-900">
      <nav className="flex items-center container mx-auto h-full justify-between">
        <h1 className="font-semibold uppercase text-lg text-gray-200">
          🔄 StableSwap
        </h1>
        <div>
          <ul className="flex items-center space-x-10 text-sm">
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">Home</a></li>
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">About Us</a></li>
            <li><a href="#!" className="text-gray-400 hover:text-gray-100">Docs</a></li>
          </ul>
        </div>
        <div>
          <Button text="Connect" bg="bg-gradient-to-r from-purple-500 to-blue-500"/>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
