import os
import dotenv
import agents

dotenv.load_dotenv()

model = os.getenv("model_gpt_4")

# assertion check to make sure you exported or set the key
openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key, "You must set OPENAI_API_KEY to run this example"


agents.user_proxy.initiate_chat(
    agents.manager,
    message=f"Create a plan for a single day of just arms including biceps and triceps.  The plan should be made for "
            f"a beginner.  The {agents.excel.name} should save this to a file named workout.csv "
            f"and {agents.document.name} should create a workout.txt"
)
