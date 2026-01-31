import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleConvert = async () => {
    if (!url) return;
    setLoading(true);
    setStatus('Processing... (Downloading & Converting)');
    setError('');

    try {
    const response = await axios.post(`http://localhost:8000/convert?link=${encodeURIComponent(url)}`, {}, {
      responseType: 'blob',
    });

    // 1. Get filename from headers
    const contentDisposition = response.headers['content-disposition'];
    let fileName = 'song.mp3'; // Fallback

    if (contentDisposition) {
      // Regex to find filename="Title Name.mp3"
      const fileNameMatch = contentDisposition.match(/filename="?(.+)"?/);
      if (fileNameMatch && fileNameMatch[1]) {
        fileName = fileNameMatch[1];
      }
    }

    // 2. Trigger download
    const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = blobUrl;
    link.setAttribute('download', fileName); // This uses the song title!
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    setStatus('Download complete!');
    } catch (err) {
      console.error(err);
      setError('Failed to convert video. Check the URL or try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-md border border-gray-700">
        <h1 className="text-3xl font-bold text-center text-red-500 mb-6">
          YT Music to MP3
        </h1>
        
        <div className="space-y-4">
          <div>
            <label htmlFor='link-input' className="block text-gray-400 text-sm font-bold mb-2">
              YouTube URL
            </label>
            <input
              id='link-input'
              type="text"
              className="w-full bg-gray-700 text-white border border-gray-600 rounded py-3 px-4 focus:outline-none focus:border-red-500 transition-colors"
              placeholder="https://music.youtube.com/watch?v=..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>

          <button
            onClick={handleConvert}
            disabled={loading || !url}
            className={`w-full font-bold py-3 px-4 rounded transition-all duration-200 
              ${loading 
                ? 'bg-gray-600 cursor-not-allowed text-gray-400' 
                : 'bg-red-600 hover:bg-red-700 text-white shadow-lg hover:shadow-red-500/50'
              }`}
          >
            {loading ? 'Converting...' : 'Convert & Download'}
          </button>

          {/* Status Messages */}
          {loading && (
            <div className="flex justify-center mt-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500"></div>
            </div>
          )}
          
          {status && !error && (
            <p className="text-green-400 text-center text-sm mt-2">{status}</p>
          )}

          {error && (
            <p className="text-red-400 text-center text-sm mt-2 bg-red-900/30 p-2 rounded">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;