import { useState } from "react";

import "./App.css";

function App() {
  const [text, setText] = useState("");

  const generateText = async () => {
    const response = await fetch("http://localhost:8080/generate");
    const data = await response.json();
    setText(data.text);
  };

  return (
    <>
      <button onClick={generateText}>Generate test</button>
      <div>{text}</div>
      <button>Enhance pronunciation</button>
    </>
  );
}

export default App;
