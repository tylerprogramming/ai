from crewai.tools import BaseTool
from pydantic import Field
import os
from supabase import create_client, Client
from pydantic import BaseModel
from typing import Type
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class SupabaseGetAllRowsInputTool(BaseModel):
    table_name: str = Field(..., description="String containing the table name.")
    
class SupabaseGetAllRowsOutputTool(BaseModel):
    result: str = Field(..., description="String containing the result.")
    count: int = Field(..., description="Integer containing the count of rows.")

class SupabaseGetAllRowsTool(BaseTool):
    name: str = "Supabase Get All Rows Tool"
    description: str = "This tool is useful for getting all rows from the Supabase database."
    
    args_schema: Type[BaseModel] = SupabaseGetAllRowsInputTool
    
    def _run(self, table_name: str) -> SupabaseGetAllRowsOutputTool:
        # Get all rows
        result = supabase.table(table_name).select("*").execute()
        
        # Get count using count() function
        result_count = supabase.table(table_name).select("*", count='exact').execute()
        
        # Convert to string representation for result and get count from metadata
        result_str = str(result.data)
        count = result_count.count

        return SupabaseGetAllRowsOutputTool(
            result=result_str,
            count=count
        )
