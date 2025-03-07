import React, { useContext, useState } from "react";
import { ApiKeyContext } from "../../contexts/ApiKeyContext"
import "./header_style.css" 


const Header = () => {

  const [inputKey, setInputKey] = useState("");
  const { saveApiKey } = useContext(ApiKeyContext);

   const handleSaveApiKey = () => {
    if (inputKey) {
      saveApiKey(inputKey);
      alert("API key Saved!")
    }
  };

   return (
    <header className="header">
      <div className="header-content">
        <div className="brand">
          <h1>FinQuery</h1>
          <span className="brand-subtitle">UK Banking Products Assistant</span>
        </div>
        <div>
          <input
            type="password"
            className="api-input"
            placeholder="Enter API Key"
            value={inputKey}
            onChange={(e) => setInputKey(e.target.value)}
          />
          <button className="set-api-btn" onClick={handleSaveApiKey}>
            Save
          </button>
        </div>
        <a href="https://console.groq.com/keys" className="link">
          Get Groq Key
        </a>
      </div>
    </header>
  );
}

export default Header

