# checkOpenAiApiKey

Currently your open Ai profile does not explicitly tell you what models you have access to.

This is a small python script to take an OpenAi Api Key and return which models it has and does 
not have access to.

Download the script and name it with a .py extension, run the script providing the api key as an 
argument. eg: python checkOpenApiKey.py sk-XXXXXXXXXXXXXX

You may need top install the openai and requests library locally first for this to work. Use pip for python v2.x 
or pip3 if you are running python 3.x. eg: pip3 install openai

We have nothing to do with open AI and can not help you get a key or if you having problems with your 
key. In that case contact open AI help directly. https://help.openai.com

Whats next: Better error logging through logging library, pip installer, automated master list of 
available models written to oaimodellist.txt

OpenAI API Key Validator

This utility is designed to validate an OpenAI API key, check connectivity to the OpenAI API, list 
available models, and check for missing required models. It also provides functionality to list available files.

Author: https://github.com/philk27 
Location:Adelaide, South Australia 
License: GNU General Public License v3.0

Usage: python checkApiKey.py [api_key]

    - api_key (optional): The OpenAI API key to use. If not provided, the utility will attempt to
                          use the API key specified in the API_KEY constant in the script, or fall
                          back to the OPENAI_API_KEY environment variable.

The utility performs the following steps:
1. Validates the provided API key or falls back to the default key.
2. Connects to the OpenAI API to check connectivity and rate limits.
3. Lists all available models.
4. Checks for missing required models based on a predefined list or a custom model list in 
oaimodellist.txt.
5. Lists available files.

Functions:
- validateApiKey(apiKey): Validates the API key format.
- connectToOpenAI(apiKey): Connects to the OpenAI API and performs connectivity and rate limit checks.
- listModels(): Lists all available models.
- checkMissingModels(availableModels): Checks for missing required models.
- listFiles(apiKey): Lists all available files.

Note: This utility requires the `openai` and `requests` libraries to be installed.

API key in hand,
Models listed, files expand,
Errors caught, so grand.
