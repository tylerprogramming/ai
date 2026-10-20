import asyncio
import json
import re

import utility
from dotenv import load_dotenv
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()  # OPENAI_API_KEY from .env

# AutoGen v0.7 has no AgentBuilder, so this example rebuilds the same idea:
#   1. ask the LLM to write a profile for every position and save them as an agent library (agents.json)
#   2. ask a "builder" agent to pick the right agents from that library for the building task
#      (structured output -> TeamSpec) and save the team to ./autogen_ab
#   3. create those agents and let them solve the execution task in a group chat

position_list = utility.position_list
agent_prompt = utility.agent_sys_msg_prompt
library_path_or_json = "./agents.json"
saved_path = "./autogen_ab"

# The default AssistantAgent system message in AutoGen v0.7
DEFAULT_SYS_MSG = "You are a helpful AI assistant. Solve tasks using your tools. Reply with TERMINATE when the task has been completed."


# The team the builder agent designs (returned as structured output)
class AgentSpec(BaseModel):
    name: str
    system_message: str


class TeamSpec(BaseModel):
    agents: list[AgentSpec] = []
    coding: bool = False  # does the team need an agent that can run Python code?


async def generate_agents(build_manager: OpenAIChatCompletionClient) -> list:
    sys_msg_list = []
    for pos in position_list:
        resp = await build_manager.create(
            [
                UserMessage(
                    content=agent_prompt.format(position=pos, default_sys_msg=DEFAULT_SYS_MSG),
                    source="user",
                )
            ]
        )

        sys_msg_list.append(
            {
                "name": pos,
                "profile": resp.content
            }
        )
    return sys_msg_list


async def build_from_library(build_manager: OpenAIChatCompletionClient, building_task: str, library: list) -> TeamSpec:
    builder = AssistantAgent(
        name="builder",
        model_client=build_manager,
        output_content_type=TeamSpec,
        system_message="You build teams of AI agents. Given a task and a library of agent profiles, pick the "
                       "2-5 agents from the library that are best suited for the task. Keep each agent's name "
                       "exactly as in the library and write a system message for it based on its profile. "
                       "Set coding to true if the team needs to write and run Python code.",
    )
    library_text = "\n".join(f"- {agent['name']}: {agent['profile']}" for agent in library)
    result = await builder.run(task=f"TASK: {building_task}\n\nAGENT LIBRARY:\n{library_text}")
    team_spec = result.messages[-1].content

    # A group chat needs at least two agents; fall back to library profiles if the builder picked too few
    for agent in library:
        if len(team_spec.agents) >= 2:
            break
        if agent["name"] not in [a.name for a in team_spec.agents]:
            team_spec.agents.append(AgentSpec(name=agent["name"], system_message=agent["profile"]))
    return team_spec


async def start_task(execution_task: str, agent_list: list, model_client: OpenAIChatCompletionClient):
    termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(12)
    group_chat = SelectorGroupChat(agent_list, model_client=model_client, termination_condition=termination)
    await Console(group_chat.run_stream(task=execution_task))


async def main():
    build_manager = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
    )
    agent_client = OpenAIChatCompletionClient(
        model="gpt-5.4-mini",
        # AutoGen 0.7.5 predates gpt-5.4-mini, so its capabilities must be given explicitly
        model_info={"vision": True, "function_calling": True, "json_output": True, "family": "gpt-5", "structured_output": True},
        # GPT-5 models only accept the default temperature (and max_completion_tokens, not max_tokens), so the old GPT-4 sampling settings were dropped
    )

    # 1. Create the agent library
    sys_msg_list = await generate_agents(build_manager)
    json.dump(sys_msg_list, open(library_path_or_json, "w"), indent=4)

    # 2. Let the builder pick agents for the task, and save the team
    team_spec = await build_from_library(build_manager, utility.building_task, sys_msg_list)
    json.dump(team_spec.model_dump(), open(saved_path, "w"), indent=4)

    agent_list = [
        AssistantAgent(
            name=re.sub(r"\W", "_", spec.name),  # agent names must be valid Python identifiers
            model_client=agent_client,
            system_message=spec.system_message + " Reply with TERMINATE when the task has been completed.",
        )
        for spec in team_spec.agents
    ]
    if team_spec.coding:
        # Like AgentBuilder's "Computer_terminal": runs the Python code the other agents write
        agent_list.append(
            # cleanup_temp_files=False keeps the files the agents write (v0.7 deletes them by default)
            CodeExecutorAgent("Computer_terminal", code_executor=LocalCommandLineCodeExecutor(work_dir="groupchat", cleanup_temp_files=False))
        )

    # 3. Run the team on the execution task
    await start_task(
        execution_task=utility.execution_task,
        agent_list=agent_list,
        model_client=agent_client,
    )

    await build_manager.close()
    await agent_client.close()


if __name__ == "__main__":
    asyncio.run(main())
