import React, { useContext } from "react";
import "../loading.css";
import { LoadingContext } from "../contexts/LoadingContext";

function Loading() {
  const { showLoading } = useContext(LoadingContext);
  return showLoading ? (
    <div className="absolute flex items-center justify-center bg-black bg-opacity-90 inset-0 z-50">
      <div class="lds-roller">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  ) : (
    ""
  );
}

export default Loading;
