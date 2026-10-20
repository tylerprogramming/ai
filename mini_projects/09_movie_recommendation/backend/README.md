# Movie Recommendation backend

Flask API for the React frontend (in the parent folder). `POST /api/recommendations` takes a text `message` or an uploaded `image` and runs a small CrewAI Flow (`movieflow/`) that searches a local Weaviate `MovieMM` collection: BM25 keyword search for text, CLIP `near_image` search for images. It returns the top 5 movies with posters.

> **Note:** Updated for Flask 3, flask-cors 6, CrewAI 1.15 and weaviate-client 4.23; the code may differ slightly from the video.

## Run it

1. Start Weaviate with the CLIP module (needs Docker):

   ```bash
   cd ../_weaviate-docker && docker compose up -d
   ```

2. Install and load the movie dataset once (downloads the data and posters):

   ```bash
   pip install -r requirements.txt
   python weaviate_setup.py   # uncomment create_collection() the first time
   ```

3. Start the API from this folder (http://localhost:5555):

   ```bash
   python app.py
   ```

4. Start the frontend from the parent folder: `npm install && npm run dev` (http://localhost:5173).

Set `FLASK_DEBUG=1` to enable Flask debug mode while developing.
