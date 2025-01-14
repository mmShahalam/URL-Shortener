import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [longUrl, setLongUrl] = useState("");
  const [customAlias, setCustomAlias] = useState("");
  const [shortUrl, setShortUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/shorten", {
        long_url: longUrl,
        custom_alias: customAlias,
      });
      setShortUrl(response.data.short_url);
    } catch (error) {
      alert(error.response.data.error || "An error occurred");
    }
  };

  return (
    <div className="App">
      <h1>URL Shortener</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Long URL"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Enter Custom Alias (optional)"
          value={customAlias}
          onChange={(e) => setCustomAlias(e.target.value)}
        />
        <button type="submit">Shorten URL</button>
      </form>
      {shortUrl && (
        <div>
          <p>Shortened URL:</p>
          <a href={shortUrl} target="_blank" rel="noopener noreferrer">
            {shortUrl}
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
