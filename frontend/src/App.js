import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [longUrl, setLongUrl] = useState("");
  const [customAlias, setCustomAlias] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setShortUrl("");

    // Validate URL format
    const isValidUrl = (url) => {
      const urlRegex = /^(https?:\/\/)?([\w\d-]+\.)+[\w]{2,}(\/\S*)?$/;
      return urlRegex.test(url);
    };

    if (!isValidUrl(longUrl)) {
      setErrorMessage("Invalid URL format. Please enter a valid URL.");
      return;
    }

    try {
      const response = await axios.post(
        "https://backend.railway.app/shorten",
        {
          long_url: longUrl,
          custom_alias: customAlias,
        }
      );
      setShortUrl(response.data.short_url);
    } catch (error) {
      setErrorMessage(
        error.response?.data?.error || "An unexpected error occurred."
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-4">URL Shortener</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Enter Long URL"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            required
          />
          <input
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Enter Custom Alias (optional)"
            value={customAlias}
            onChange={(e) => setCustomAlias(e.target.value)}
          />
          <button
            type="submit"
            className="w-full bg-blue-500 text-white font-bold py-2 rounded-lg hover:bg-blue-600 transition duration-200"
          >
            Shorten URL
          </button>
        </form>
        {errorMessage && (
          <p className="mt-4 text-red-500 text-center">{errorMessage}</p>
        )}
        {shortUrl && (
          <div className="mt-4 text-center">
            <p className="text-gray-700">Shortened URL:</p>
            <a
              href={`https://domain.com/${shortUrl}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 font-bold hover:underline"
            >
              https://domain.com/{shortUrl}
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;