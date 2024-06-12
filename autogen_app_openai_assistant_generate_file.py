#https://github.com/microsoft/autogen/blob/main/notebook/agentchat_oai_code_interpreter.ipynb
#Auto Generated Agent Chat: GPTAssistant with Code Interpreter
#https://www.youtube.com/watch?v=haDtYk7pz0c

#Code modified from simple, single GPT Assistant call to A) File Upload manually on Assistants and B) Failed ttempts at Integrating multiple Assistants in GroupChat.

import io
import os
from dotenv import load_dotenv

from IPython.display import display
from PIL import Image

import autogen
from autogen.agentchat import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

from openai import OpenAI

load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo" #EDIT MODEL
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
llm_config = {"config_list": config_list}
client = OpenAI()

#Upload file to the assistant
file = client.files.create(
    file=open("Financial-Sample-Much-Shortened.csv", "rb"),
    purpose='assistants'
)

# Get an agent equipped with code interpreter. It creates a new agent if an identical one is not found.
data_analyst = GPTAssistantAgent(
    name="Data Analyst",
    llm_config=llm_config,
    assistant_config={
        "tools": [{"type": "code_interpreter"}],
        "code_interpreter": {
            "file_ids": [file.id]
        }
    },
    instructions="You are an expert financial data analyst. Based on the file and it's data schema, e.g. columns, you plan comprehensive financial data analysis on the file. You then send this financial analysis plan further to next agent, with instructions to properly carry it out.",
)

coder_assistant = GPTAssistantAgent(
    name="Coder Assistant",
    llm_config=llm_config,
    assistant_config={
        "tools": [{"type": "code_interpreter"}],
        "code_interpreter": {
            "file_ids": [file.id]
        }
    },
    instructions="You are an expert at writing python code to perform data analysis. You receive financial data analysis plan from another agent and you carry it out on the file. You must as output return the complete results of the analysis along with interesting insights and potential visualizations.",
)

# user_proxy = UserProxyAgent(
#     name="user_proxy",
#     is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
#     code_execution_config={
#         "work_dir": "coding",
#         "use_docker": False,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
#     },
#     human_input_mode="NEVER",
# )

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="NEVER",
)

# user_proxy.initiate_chat(
#     gpt_assistant,
#     message="Analyze the file 'Financial-Sample-Much-Shortened' and share insights. Please share a download link to a file with more info",
#     is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
#     human_input_mode="NEVER",
#     clear_history=True,
#     max_consecutive_auto_reply=1,
# )

groupchat = autogen.GroupChat(agents=[user_proxy, data_analyst, coder_assistant], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

#gpt_assistant.delete_assistant()

# file_path = "C:\Users\TimJ1\Documents\Financial_Sample_Much_Shortened.csv"
# file_path = "C:/Users/TimJ1/Documents\Financial_Sample_Much_Shortened.csv"
file_path_local = "C:\\Users\\TimJ1\\Documents\\Financial_Sample_Much_Shortened.csv"
file_name = file.filename
file_id = file.id

user_proxy.initiate_chat(
    manager,
    message=f"Workflow flow and description. Two GPT Assistants work together. One, Data Analyst, will plan a comprehensive analysis on the file: {file_name}. It will then send instructions to carry out this comprehensive analysis plan to the next agent, Coder Assistant, who will return the results of the analysis.",
)
# type exit to terminate the chat