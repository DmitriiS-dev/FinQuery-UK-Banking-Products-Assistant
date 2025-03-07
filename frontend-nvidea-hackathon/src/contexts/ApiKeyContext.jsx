import React, { createContext, useState } from "react";

export const ApiKeyContext = createContext();

export const ApiKeyProvider = ({ children }) => {
  const [apiKey, setApiKey] = useState(""); 

  // Function to save the API key
  const saveApiKey = (key) => {
    setApiKey(key);
  };

  return (
    <ApiKeyContext.Provider value={{ apiKey, saveApiKey }}>
      {children}
    </ApiKeyContext.Provider>
  );
};
