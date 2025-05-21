import { useState } from "react";

import "./App.css";

// Helper function to strip SSML/HTML tags
const stripSsmlTags = (ssml: string): string => {
  if (!ssml) return "";
  // Replace any <...> or </...> with an empty string
  // Add a space for <p> and <br> tags to represent paragraph/line breaks better
  return ssml
    .replace(/<p>/gi, "\n") // Replace <p> with a newline
    .replace(/<br\s*\/?>/gi, "\n") // Replace <br> with a newline
    .replace(/<[^>]+>/g, "") // Remove all other tags
    .trim();
};

function App() {
  const [text, setText] = useState("");
  const [audioFile, setAudioFile] = useState("");

  const createStory = async () => {
    const response = await fetch("http://127.0.0.1:5001/api/generate_story", {
      method: "GET",
    });
    const data = await response.json();
    const plainText = stripSsmlTags(data.ssml_text);
    setText(plainText || `Genre: ${data.genre || 'N/A'}`);
    if (data.audio_base64) {
      setAudioFile(`data:audio/mp3;base64,${data.audio_base64}`);
    } else {
      setAudioFile("");
    }
  };

  return (
    <>
      <button style={{ margin: "5px" }} onClick={createStory}>
        Create a story
      </button>
      <textarea
        style={{ width: "500px", height: "500px", display: "block" }}
        readOnly
        value={text}
      />
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
