from crewai.tools import BaseTool
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class SupabaseGetRowTool(BaseTool):
    name: str = "Supabase Get Row Tool"
    description: str = "This tool is useful for getting a row from the Supabase database."

    def _run(self, table_name: str, column_name: str, value: str) -> str:
        result = supabase.table(table_name).select("*").eq(column_name, value).execute()
        return result
