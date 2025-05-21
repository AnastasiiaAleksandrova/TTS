import { useState } from "react";

import "./App.css";

function App() {
  const [text, setText] = useState("");

  const generateText = async () => {
    const response = await fetch("http://localhost:8080/generate");
    const data = await response.json();
    setText(data.text);
  };

  const addMarkup = async () => {
    const response = await fetch("http://localhost:8080/add-markup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setText(data.text);
  };
  const generateSpeech = async () => {
    const response = await fetch("http://localhost:8080/generate-speech", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    const audio = new Audio(data.audioUrl);
    audio.play();
  };
  return (
    <>
      <button style={{ margin: "5px" }} onClick={generateText}>
        Create a story
      </button>
      <textarea
        style={{ width: "500px", height: "500px", display: "block" }}
        readOnly
      >
        {text}
      </textarea>
      <button style={{ margin: "5px" }} onClick={addMarkup}>
        Add markup
      </button>
      <button style={{ margin: "5px" }} onClick={generateSpeech}>
        Generate speech
      </button>
    </>
  );
}

export default App;
