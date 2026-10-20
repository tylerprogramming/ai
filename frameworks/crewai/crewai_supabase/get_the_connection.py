import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Add debug prints to verify environment variables
print(f"URL: {url}")
print(f"Key: {'*' * len(key) if key else 'None'}")  # Masked key for security

supabase: Client = create_client(url, key)

result = supabase.table("leads").select("*").execute()

print(f"Insert result: {result}")

