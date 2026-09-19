import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { MovieGrid } from './components/MovieGrid';
import { MovieModal } from './components/MovieModal';
import { Movie } from './types/movie';
import './App.css';

const SAMPLE_QUERIES = [
  "Find action movies with cars",
  "Movies with lots of green scenery",
  "Sci-fi movies in space",
  "Movies about cooking",
  "Romantic comedies in Paris",
  "Movies with superheroes"
];

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [messages, setMessages] = useState<{ text: string, sender: 'user' | 'bot', recommendations?: Movie[] }[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleSearch = async (image: File | null) => {
    if (!image && !searchQuery.trim()) return;

    try {
      const formData = new FormData();
      if (image) {
        formData.append('image', image);
      }
      if (searchQuery.trim()) {
        formData.append('message', searchQuery);
      }

      const response = await fetch('http://localhost:5555/api/recommendations', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      console.log(data);
      
      setMovies(data.movies);
      
      setMessages(prevMessages => [
        ...prevMessages,
        {
          text: 'Here are some movie recommendations for you:',
          sender: 'bot',
          recommendations: data.movies
        }
      ]);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setMessages(prevMessages => [
        ...prevMessages,
        {
          text: 'Sorry, there was an error getting recommendations.',
          sender: 'bot'
        }
      ]);
    }
    
    setSearchQuery('');
  };

  const handleSampleQuery = async (query: string) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('message', query);

      const response = await fetch('http://localhost:5555/api/recommendations', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setMovies(data.movies || []);
      
      setMessages(prevMessages => [
        ...prevMessages,
        {
          text: 'Here are some movie recommendations for you:',
          sender: 'bot',
          recommendations: data.movies
        }
      ]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prevMessages => [
        ...prevMessages,
        {
          text: 'Sorry, there was an error getting recommendations.',
          sender: 'bot'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Movie Recommendations</h1>
          <p className="text-gray-400 text-lg">
            Discover your next favorite movie
          </p>
        </div>
        
        <div className="flex justify-center mb-12">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            onSubmit={handleSearch}
          />
        </div>

        {/* Sample Queries Section */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-4 justify-center">
            {SAMPLE_QUERIES.map((query) => (
              <button
                key={query}
                onClick={() => handleSampleQuery(query)}
                className="px-6 py-3 bg-neutral-900 text-gray-300 rounded-full 
                           border border-neutral-700 hover:bg-neutral-800 
                           transition-colors duration-200"
              >
                {query}
              </button>
            ))}
          </div>
        </div>

        {/* Existing upload section */}
        <div className="flex flex-col items-center gap-4 mb-8">
          {/* ... existing upload UI ... */}
        </div>

        {loading ? (
          <div className="text-center">Loading...</div>
        ) : (
          <MovieGrid 
            movies={movies} 
            onSelectMovie={setSelectedMovie}
          />
        )}

        {movies.length === 0 && searchQuery && (
          <div className="text-center text-gray-400 mt-12">
            Start typing to get movie recommendations
          </div>
        )}

        {selectedMovie && (
          <MovieModal
            movie={selectedMovie}
            onClose={() => setSelectedMovie(null)}
          />
        )}
      </div>
    </div>
  );
}

export default App;