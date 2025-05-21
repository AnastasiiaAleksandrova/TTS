import { useState } from "react";

import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [audioFile, setAudioFile] = useState("");

  const createStory = async () => {
    const response = await fetch("http://localhost:8080/create-and-play", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setText(data.text);
    setAudioFile(data.audioFile);
  };

  return (
    <>
      <button style={{ margin: "5px" }} onClick={createStory}>
        Create a story
      </button>
      <textarea
        style={{ width: "500px", height: "500px", display: "block" }}
        readOnly
      >
        {text}
      </textarea>
      <audio
        controls
        style={{ width: "500px", display: "block", margin: "5px" }}
        src={audioFile}
      >
        Your browser does not support the audio element.
      </audio>
    </>
  );
}

export default App;
