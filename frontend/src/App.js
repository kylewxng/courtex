import React, { useState } from "react";
import "./App.css";
import CourtDiagram from "./CourtDiagram";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [plays, setPlays] = useState([]);

  return (
    <div className="app">
      <h1>Courtex</h1>
      <p className="subtitle">AI-powered NBA play analysis</p>
      <div className="search">
        <input
          type="text"
          placeholder="Ask about any NBA play..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          disabled={loading}
          onClick={async () => {
            setLoading(true);
            try {
              const response = await fetch(
                "https://uuom4bb4qjj4s5vikklkowtgae0xksww.lambda-url.us-west-2.on.aws/query",
                {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({ question }),
                },
              );
              const data = await response.json();
              setAnswer(data.answer);
              setPlays(data.plays);
              console.log(data.plays);
            } catch (error) {
              console.error("Error fetching answer:", error);
            } finally {
              setLoading(false);
            }
          }}
        >
          {loading ? "Loading..." : "Search"}
        </button>
      </div>
      {answer && (
        <div className="answer">
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      )}
      {plays.length > 0 && (
        <div className="court">
          <p className="court-label">Shot distribution</p>
          <CourtDiagram plays={plays} />
        </div>
      )}
    </div>
  );
}

export default App;
