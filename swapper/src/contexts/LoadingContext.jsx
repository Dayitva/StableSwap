import { useState, createContext } from "react";

const LoadingContext = createContext(false);

function LoadingProvider(props) {
  const [showLoading, setShowLoading] = useState(false);
  const values = { showLoading, setShowLoading };

  return (
    <LoadingContext.Provider value={values}>
      {props.children}
    </LoadingContext.Provider>
  );
}

export { LoadingContext, LoadingProvider };
