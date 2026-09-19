from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get("/fetch-todo")
async def fetch_todo():
    async with httpx.AsyncClient() as client:
        response = await client.get('<https://jsonplaceholder.typicode.com/todos>')
        json_data = response.json()
        return json_data[:5]


@app.get("/fetch-users")
async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('<https://jsonplaceholder.typicode.com/users>')
        json_data = response.json()
        return json_data






