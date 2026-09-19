from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from supabase_tools import (
    supabase_get_row_tool, 
    supabase_get_all_rows_tool, 
    supabase_insert_row_tool, 
    supabase_delete_row_tool, 
    supabase_update_row_tool
)

from crewai_tools import FileWriterTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

text_knowledge = open("knowledge/table_info.txt", "r").read()

file_writer = FileWriterTool(
    file_path="./knowledge/table_info.txt",
    name="Table Info"
)

load_dotenv()

# Create instances of the tools
get_row_tool = supabase_get_row_tool()  # Instantiate the tool
get_all_rows = supabase_get_all_rows_tool()
insert_row = supabase_insert_row_tool()
delete_row = supabase_delete_row_tool()
update_row = supabase_update_row_tool()

llm = LLM(model="gpt-4o", temperature=0, api_key="sk-111")

# Create an agent with supabase tools
agent = Agent(
    role="Supabase Agent",
    goal="You will perform executions on the Supabase database.",
    backstory=f"""
        You are a master at performing executions on the Supabase database.
        You are able to perform the following operations:
        - Get a row from the database.
        - Get all rows from the database.
        - Insert a row into the database.
        - Delete a row from the database.
        - Update a row in the database.
        
        For insert operations, the input should be a string containing the input to insert, all columns data should be in a data dict field in the string.
        
        For delete operations, try to get the row you are deleting first, ensure it exists, then delete it.  If the user doesn't provide 
        enough information to delete a row, then ask for more information and mention that value didn't return any rows.  Try to get all rows and provide 
        the user with ones that are similar with the column name. 
        
        If you need information to get the right information for a tool such as correct table names, you can use the knowledge source.
        
        All boolean columns should always generate answers with "True/False" in double quotation marks.
        If a date field has no data, or no data is provided, then don't include it in the data you are inserting.
        
        If there is a generated id for the primary key, then make sure to include it in the data you are inserting.
        Make sure to always get the rows of data for the table to make sure we have all the columns necessary.
        
        You must use the tools provided to you to perform the operations.  If you are performing an operation 
        that is not just retrieving data, then make sure you have the correct format for the tables with columns.  If
        the data coming in doesn't have all the necessary information but is also not needed, then fill in defaults.
        
        If you need to update the table info, then use the file writer tool to update the file.
        
        Here is the table info:
        A list of tables and their columns: {text_knowledge}
    """,
    tools=[get_row_tool, get_all_rows, insert_row, delete_row, update_row, file_writer],  # Pass the tool instance, not the class
    verbose=True,
    allow_delegation=False,
    # knowledge_sources=[text_knowledge],
    llm=llm
)

task = Task(
    description="Answer the following questions about the database: {question}.",
    expected_output="You are to return the result of the operation you performed.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    # knowledge_sources=[text_knowledge],
)

while True:
    question = input("Input: ")
    result = crew.kickoff(inputs={"question": question})
    print(result)