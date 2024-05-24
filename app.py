#Credit to 'Mervin Praison' and his YouTube videos (https://www.youtube.com/watch?v=DDDXO_Y_YAI) for sample code used to inspire this project. Same goes for documentation and examples from CrewAI and 'DeepLearning.AI' (https://learn.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai)

#pip install open-interpreter crewai gradio langchain langchain-openai crewai_tools

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from interpreter import interpreter
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from IPython.display import Markdown

# 1. Configuration and Tools
load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0.5

llm = ChatOpenAI(model=model_name, temperature=temp, api_key=openai_api_key) #Could leave out API key if specified in ENV variables.
interpreter.auto_run = True
interpreter.llm.model = "openai/" + model_name
#interpreter.llm.context_window = {token limit}
#interpreter.llm.max_tokens = {max tokens per response}

class CLITool:
    @tool("Executor")
    def execute_cli_command(command: str):
        """Create and Execute code using Open Interpreter."""
        result = interpreter.chat(command)
        return result

# 2. Creating an Agent for CLI tasks
cli_agent = Agent(
    role='Software Engineer',
    goal='Ability to perform CLI operations, write programs and execute using Executor Tool.',
    backstory='Expert in command line operations and automating tasks.',
    tools=[CLITool.execute_cli_command],
    verbose=True,
    allow_delegation=True,
)

# 3. Defining a Task for CLI operations
cli_task = Task(
    description='Identify the OS and some system info on this Windows machine',
    expected_output='A printable string, status on the results of your task, i.e. information about my OS, etc.',
    agent=cli_agent,
    tools=[CLITool.execute_cli_command]
)

# 4. Creating a Crew with CLI focus (alt: "process=Process.hierachical,")
cli_crew = Crew(
    agents=[cli_agent],
    tasks=[cli_task],
    process=Process.sequential, 
    manager_llm=llm,
    verbose=True
)

# 5. Run the Crew (opt: input in kickoff param)
result = cli_crew.kickoff()
Markdown(result)