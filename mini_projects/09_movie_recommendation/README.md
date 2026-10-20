# Movie Recommendation

Describe a movie or upload an image, and get five recommendations with posters.

- **Frontend** (this folder): React + TypeScript + Vite + Tailwind CSS.
- **Backend** (`backend/`): a Flask API that runs a CrewAI Flow to search a local Weaviate database (keyword search for text, CLIP image search for uploads).
- **Database** (`_weaviate-docker/`): Weaviate with the CLIP module, run with Docker.

> **Note:** Updated to Vite 8 and Tailwind CSS 4 (the Vite 5 dev server had security fixes only in newer majors), and the backend to Flask 3 / CrewAI 1.15. The code may differ slightly from the video.

## Run it

1. Start Weaviate, load the data and start the API: see [`backend/README.md`](backend/README.md).
2. Start the frontend from this folder:

   ```bash
   npm install
   npm run dev
   ```

   Open http://localhost:5173. It calls the API at http://localhost:5555.
