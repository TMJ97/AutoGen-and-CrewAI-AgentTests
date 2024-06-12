#https://github.com/microsoft/autogen/blob/main/notebook/agentchat_human_feedback.ipynb
#Auto Generated Agent Chat: Task Solving with Code Generation, Execution, Debugging & Human Feedback

#pip install pyautogen

import json
import os
from dotenv import load_dotenv
import autogen


load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0

# config_list = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     file_location=".",
#     filter_dict={
#         "model": ["gpt-3.5-turbo", "gpt-35-turbo", "gpt-4", "gpt4", "gpt-4-32k", "gpt-4-turbo"],
#     },
# )

# When using a single openai endpoint, you can use the following:
config_list = [{"model": model_name, "api_key": openai_api_key}]

# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,
        "config_list": config_list,
    },
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "use_docker": False
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

# Load the content of the file to analyze
# file_path = "Financial-Sample-Much-Shortened.csv" #Relative or absolute file path?
# with open(file_path, "r") as file:
#     file_content = file.read()

problem_to_solve = """
Perform write and run code to perform financial data analysis on this file "Financial-Sample-Much-Shortened.csv"
"""

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(assistant, message=problem_to_solve)

#print(user_proxy.chat_messages[assistant])
#json.dump(user_proxy.chat_messages[assistant], open("conversations.json", "w"), indent=2)