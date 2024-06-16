#https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_research/
#Perform Research with Multi-Agent Group Chat

#pip install pyautogen

import os
from dotenv import load_dotenv
import autogen

load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0

# When using a single openai endpoint, you can use the following:
config_list = [{"model": model_name, "api_key": openai_api_key}]

llm_config = {"config_list": config_list, "cache_seed": 42, "temperature": temp}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
""",
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=llm_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=llm_config,
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER", #NEVER, ALWAYS, TERMINATE
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

sub_task_area_1 = "LLM applications"
sub_task_area_2 = "Agent Architecture"
task = f"Find papers on {sub_task_area_1} from arxiv in last month, create a markdown table of different domains."

user_proxy.initiate_chat(
    manager,
    message=f"""{task}""",
)