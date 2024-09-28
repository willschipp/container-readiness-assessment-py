import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('/api/languages')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  return (
    <div className="App">
      <h1>React + Flask App</h1>
      <p>Message from Flask: {data.languages}</p>
    </div>
  );
}

export default App;