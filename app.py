#Credit to 'Mervin Praison' and his YouTube videos (https://www.youtube.com/watch?v=DDDXO_Y_YAI) for sample code used to inspire this project. Same goes for documentation and examples from CrewAI and 'DeepLearning.AI' (https://learn.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai)

#pip install open-interpreter crewai gradio langchain langchain-openai crewai_tools

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import CSVSearchTool, FileReadTool
from interpreter import interpreter
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from IPython.display import Markdown

# 1. Configuration and Tools
load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0

llm = ChatOpenAI(model=model_name, temperature=temp, api_key=openai_api_key) #Could leave out API key if specified in ENV variables.
interpreter.auto_run = True
interpreter.llm.model = "openai/" + model_name
#interpreter.llm.context_window = {token limit}
#interpreter.llm.max_tokens = {max tokens per response}
interpreter.llm.max_retries = 20

class CLITool:
    @tool("Executor")
    def execute_cli_command(command: str):
        """Create and Execute code using Open Interpreter."""
        result = interpreter.chat(command)
        return result
    
CSVSearchTool = CSVSearchTool(csv="C:/Users/TimJ1/Downloads/Financial-Sample-Much-Shortened.csv")
FileReadTool = FileReadTool(file_path="C:/Users/TimJ1/Downloads/Financial-Sample-Much-Shortened.csv")


# 2. Creating Agents
data_analyst_planner = Agent(
    role='Financial Data Analyst Planner',
    goal='Ability to plan an analysis of given input data (a CSV file). Read the entirety of the CSV file using the FileReadTool. Summarize the data. Create a comprehensive plan for EDA (exploratory data analysis). Pass this data analysis summarization and plan on to the next agent',
    backstory='Expert business analyst and data scientist, able to perform comprehensive data analysis for any given type of financial data in a CSV file.',
    tools=[FileReadTool],
    verbose=True,
    allow_delegation=True,
)

data_analyst_executor = Agent(
    role='Financial Data Analyst Executor',
    goal='Receive a summary of data for analysis and a corresponding data analysis plan. First, you receive the summary and plan as a string. Then you can access the entire file using the FileReadTool (all of the data must be included in the analysis). Then you write and run code to analyse the data (access any time with FileReadTool, perhaps storing it somewhere you can remember it or access it with the code), using the Executor tool. Finally, you can then evaluate the code results and ultimately complete the data analysis, returning bullet-point observations, insights and even recommendations.',
    backstory='Expert business analyst and data scientist, able to receive a comprehensive data analysis plan and run analysis code for any given type of input data in a CSV file, ultimately finishing an exploratory data analysis.',
    tools=[FileReadTool, CLITool.execute_cli_command],
    verbose=True,
    allow_delegation=True,
)

# 3. Defining Tasks
read_and_plan_data_analysis = Task(
    description='Read and summarize the entirety of the given file contents, using the FileReadTool. Return both a summary of the data and a comprehensive data analysis plan for this type of data.',
    expected_output='A summary of the data in the file and a comprehensive data analysis plan.',
    agent=data_analyst_planner,
    tools=[FileReadTool],
)

carry_out_data_analysis = Task(
    description='Based on the received information (summary of data for analysis and a comprehensive data analysis plan), write and run code using the Executor tool to complete the data analysis and return final results including observations, insights and recommendations. Access the input data via the FileReadTool, reading the entire file content as all of it is relevant.',
    expected_output='The results of the comprehensive data analysis including observations, insights, as well as considerations, thoughts, and recommendations.',
    agent=data_analyst_executor,
    tools=[FileReadTool, CLITool.execute_cli_command],
)

# 4. Creating a Crew with CLI focus (alt: "process=Process.hierachical,")
data_crew = Crew(
    agents=[data_analyst_planner, data_analyst_executor],
    tasks=[read_and_plan_data_analysis, carry_out_data_analysis],
    process=Process.sequential, 
    manager_llm=llm,
    verbose=True,
)

# 5. Run the Crew (opt: input in kickoff param)
result = data_crew.kickoff()
Markdown(result)