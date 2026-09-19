from crewai.tools import BaseTool
from pydantic import Field
import os
from supabase import create_client, Client
from pydantic import BaseModel
from typing import Type

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class SupabaseUpdateRowInputTool(BaseModel):
    table_name: str = Field(..., description="String containing the table name.")
    data: dict = Field(..., description="Dictionary containing the data to insert.")
    column_name: str = Field(..., description="String containing the column name.")
    value: str = Field(..., description="String containing the value.")

class SupabaseUpdateRowTool(BaseTool):
    name: str = "Supabase Update Row Tool"
    description: str = "This tool is useful for updating a row in the Supabase database."
    
    args_schema: Type[BaseModel] = SupabaseUpdateRowInputTool

    def _run(self, table_name: str, data: dict, column_name: str, value: str) -> str:
        result = supabase.table(table_name).update(data).eq(column_name, value).execute()
        return result
