import weaviate
import weaviate.classes.query as wq


from dotenv import load_dotenv

load_dotenv()

import os

api_key = os.getenv("OPENAI_API_KEY")

def weaviate_search(query):
    headers = {
        "X-OpenAI-Api-Key": "sk-111"
    }

    client = weaviate.connect_to_local(headers=headers)
    
    # Get the collection
    movies = client.collections.get("MovieMM")

    # Perform query
    response = movies.query.bm25(
        query=query, 
        limit=5, 
        return_metadata=wq.MetadataQuery(distance=True),
        return_properties=["title", "release_date", "tmdb_id", "poster", "vote_average", "overview"]
    )

    # Create a list to store the results
    results = []
    
    # Inspect and collect the response
    for o in response.objects:
        poster_url = f"data:image/jpeg;base64,{o.properties['poster']}" if o.properties['poster'] else ""
        # Collect the results in a dictionary
        movie = {
            "title": o.properties["title"],
            "voteAverage": o.properties["vote_average"],
            "posterUrl": poster_url,
            "year": o.properties["release_date"].year,
            "summary": o.properties["overview"]
        }
        
        results.append(movie)
        
    client.close()
    
    return results

    