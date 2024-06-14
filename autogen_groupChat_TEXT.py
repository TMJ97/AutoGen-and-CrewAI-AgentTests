#Group Chat with Coder and Visualization Critic
#https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat_vis.ipynb

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import Image

import autogen

import json
import os
from dotenv import load_dotenv

load_dotenv() #.env file might not be in use...
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-0125"
temp = 0

# When using a single openai endpoint, you can use the following:
config_list = [{"model": model_name, "api_key": openai_api_key}]