import React, { useState } from "react";

const API_URL = "https://8217r5vnq5.execute-api.us-east-1.amazonaws.com";

function App() {
  const [file, setFile] = useState(null);
  const [voice, setVoice] = useState("Joanna");
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [message, setMessage] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  // Handle file selection
  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  // Submit file to backend
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please upload a text file.");
      return;
    }

    setMessage("Processing...");
    setIsProcessing(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("voice", voice);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData, // Sending file as FormData
      });

      const data = await response.json();

      if (response.ok && data.download_url) {
        setDownloadUrl(data.download_url);
        setMessage("Conversion successful! Click the button to download.");
      } else {
        setMessage("Error: Could not process request.");
      }
    } catch (error) {
      setMessage("Error: " + error.message);
    }

    setIsProcessing(false);
  };

  return (
    <div style={{ maxWidth: "500px", margin: "50px auto", textAlign: "center" }}>
      <h2>Text-to-Speech Converter</h2>

      {/* File Upload */}
      <input type="file" accept=".txt" onChange={handleFileUpload} style={{ marginBottom: "10px" }} />

      {/* Voice Selection */}
      <select
        value={voice}
        onChange={(e) => setVoice(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      >
        <option value="Joanna">Joanna (Female)</option>
        <option value="Matthew">Matthew (Male)</option>
      </select>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={isProcessing}
        style={{ width: "100%", padding: "10px", background: "blue", color: "white", border: "none" }}
      >
        {isProcessing ? "Processing..." : "Convert to Speech"}
      </button>

      {/* Status Message */}
      {message && <p style={{ marginTop: "20px" }}>{message}</p>}

      {/* Download Button */}
      {downloadUrl && (
        <a href={downloadUrl} download="speech.mp3">
          <button style={{ marginTop: "20px", padding: "10px", background: "green", color: "white", border: "none" }}>
            Download Audio
          </button>
        </a>
      )}
    </div>
  );
}

export default App;
