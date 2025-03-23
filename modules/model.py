"""
Configuration and AWS Interaction Module

This module provides functionality related to loading configuration data from a JSON file and interacting with AWS services.

Attributes:
    project_root (str): The root directory of the project.
    config_file_path (str): The path to the config.json file.

Functions:
    query_bedrock_sonet(prompt):
        Query the Bedrock SONET model with the provided prompt.
"""

import json
import os
import boto3
from modules.utils import load_config_data

from ollama import Client
from ollama import ChatResponse


def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

# Get the path to the config.json file
project_root = os.path.dirname(os.path.dirname(__file__))  # Navigate 2 levels up from the script directory
config_file_path = os.path.join(project_root, 'config.json')


def query_bedrock_sonet(prompt):
    """
    Query the Bedrock SONET model with the provided prompt.

    Args:
        prompt (str): The prompt to query the Bedrock SONET model.

    Returns:
        dict: Response from the Bedrock SONET model.
    """
    client = Client(
        host='http://DESKTOP-9NKPN1L.home.arpa:11434',
    )
    # Load the AWS credentials data

    model = 'gemma3:1b'
    ctx = next_power_of_2(len(prompt))
    print('ctx', len(prompt), ctx)
    user_input = prompt
    messages = []
    while True:
         # Add the response to the messages to maintain the history
        messages += [
            {'role': 'user', 'content': user_input}];        
        stream  = client.chat(model=model, options={'num_ctx': ctx}, messages=messages ,    stream=True )

        response = ''
        for chunk in stream:
             response += chunk['message']['content']
             print(chunk['message']['content'], end='', flush=True)

        messages += [
            {'role': 'assistant', 'content':response},
        ]
        user_input = input('\nChat: ')
       

    return response.message.content
