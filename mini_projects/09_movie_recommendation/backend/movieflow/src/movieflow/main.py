#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from weaviate_image_search import weaviate_image_search
from weaviate_search import weaviate_search
import json
import base64

class MovieState(BaseModel):
    image_b64: str | None = None
    query: str | None = None
    movies: list[dict] = []


class MovieFlow(Flow[MovieState]):

    @start()
    def recommend_movies(self):
        print("Starting movie recommendation")
        
        # Check if we have valid inputs
        if not self.state.image_b64 and not self.state.query:
            print("No valid input provided")
            return None
            
        if self.state.query and self.state.query.strip():
            print(f"Using text search with query: {self.state.query}")
            result = weaviate_search(self.state.query)
        elif self.state.image_b64:
            print("Using image search")
            result = weaviate_image_search(self.state.image_b64)
        else:
            print("No valid search criteria")
            return None

        self.state.movies = result
        return result


def kickoff(request_files=None, request_form=None):
    """
    Process both image and text inputs from the request
    
    Args:
        request_files: The files dictionary from the request
        request_form: The form dictionary from the request
    
    Returns:
        list: List of recommended movies or None if no valid input
    """
    inputs = {}
    
    # Process image if it exists
    if request_files and 'image' in request_files:
        image = request_files['image']
        image_content = image.read()
        inputs["image_b64"] = base64.b64encode(image_content).decode('utf-8')
    
    # Process text query if it exists
    if request_form:
        message = request_form.get('message', '').strip()
        if message:
            inputs["query"] = message
    
    # Only proceed if we have at least one valid input
    if not inputs:
        return None
        
    movie_flow = MovieFlow()
    result = movie_flow.kickoff(inputs=inputs)
    return result
