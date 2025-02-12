import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState({
    pages: [],
    keywords: [],
    errors: [],
    total_time: 0
  });

  useEffect(() => {
    fetch('/output.json')
      .then(response => response.json())
      .then(jsonData => setData(jsonData))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <h1>SEO Analysis Results</h1>
      
      <div className="stats">
        <p>Total Time: {data.total_time?.toFixed(2)}s</p>
        <p>Total Pages: {data.pages?.length}</p>
        <p>Total Errors: {data.errors?.length}</p>
      </div>

      <div className="table-container">
        <h2>Pages Analyzed</h2>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Content Hash</th>
            </tr>
          </thead>
          <tbody>
            {data.pages.map((page, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{page.content_hash}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {data.errors.length > 0 && (
          <>
            <h2>Errors</h2>
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Error Message</th>
                </tr>
              </thead>
              <tbody>
                {data.errors.map((error, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{error}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
