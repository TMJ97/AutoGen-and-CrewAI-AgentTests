#https://github.com/microsoft/autogen/blob/main/notebook/agentchat_human_feedback.ipynb
#Auto Generated Agent Chat: Task Solving with Code Generation, Execution, Debugging & Human Feedback

#v2 (link above) turned into GroupChat like:
##Group Chat with Coder and Visualization Critic
##https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat_vis.ipynb

#pip install pyautogen

import json
import os
from dotenv import load_dotenv
import autogen

load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0

# When using a single openai endpoint, you can use the following:
config_list = [{"model": model_name, "api_key": openai_api_key}]

llm_config = {"config_list": config_list, "cache_seed": 42}

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="ALWAYS",
)

filepath_perfect = "C:\\Users\\TimJ1\\Documents\\Financial_Sample_Much_Shortened.csv" #Remember to escape the \ sign with the escape sign, \...
filepath_unclean = "C:\\Users\\TimJ1\\Documents\\Financial_Sample_Much_Shortened_Err.csv" #Remember to escape the \ sign with the escape sign, \...

# create AssistantAgent instances
data_visualizer = autogen.AssistantAgent(
    name="Data Visualizer",
    system_message="""Data Visualizer. You are a helpful assistant highly skilled in data science and financial data analysis.
    You must visualize a specific insight from your fellow agent, Data Analyzer. Refer to the specific data file for correct visulization. Suggest code to perform the visualization on the specific file, passing the User_proxy for code execution. You MUST always provide the entirety of the code. Instruct the User_proxy to execute the code resulting in an image.
""",
    llm_config=llm_config, 
)
data_analyzer = autogen.AssistantAgent(
    name="Data Analyzer",
    system_message="""Data Analyzer. You are a helpful assistant highly skilled in data science and financial data analysis.
    You must perform data analysis on a specific file. Suggest code to perform the data analysis on the specific file, passing the User_proxy for code execution. You MUST always provide the entirety of the code. Instruct the User_proxy to return results to you for final evaluation. You then output analysis insights. Send the most interesting insight to the Data Visualizer for visualization with clear instructions.
""",
    llm_config=llm_config, 
)

### Load the content of the file to analyze
## file_path = "Financial-Sample-Much-Shortened.csv" #Relative or absolute file path?
## with open(file_path, "r") as file:
##     file_content = file.read()

groupchat = autogen.GroupChat(agents=[user_proxy, data_analyzer, data_visualizer], messages=[], max_round=25)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message=f"Perform data analysis along with a single visualiztion on the file here: {filepath_perfect}. The User_proxy will always execute the code written by the other two agents. Both agents, Data Cleaner and Data Analyzer, must always send code in its entirety ready for execution to the User_proxy, and follow with instructions to execute code and return results. Data Analyzer should perform inital data analysis and provide insigts, Data Visualizer should visualize the most appropriate insight.",
)
# type exit to terminate the chat