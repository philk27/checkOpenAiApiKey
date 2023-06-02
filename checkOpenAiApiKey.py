# Project: OpenAI API Key Validator
# Version: 0.4.0
# Author: Philip Kalogeras
# Location: Adelaide, South Australia
# License: GNU General Public License v3.0
# Github: https://github.com/philk27/checkOpenAiApiKey
# Last Modified: 02 June 2023

"""
OpenAI API Key Validator

This utility is designed to validate an OpenAI API key, check connectivity to the OpenAI API,
list available models, and check for missing required models. It also provides functionality
to list available files.

Usage:
    python checkApiKey.py [api_key]

    - api_key (optional): The OpenAI API key to use. If not provided, the utility will attempt to
                          use the API key specified in the API_KEY constant in the script, or fall
                          back to the OPENAI_API_KEY environment variable.

The utility performs the following steps:
1. Validates the provided API key or falls back to the default key.
2. Connects to the OpenAI API to check connectivity and rate limits.
3. Lists all available models.
4. Checks for missing required models based on a predefined list or a custom model list.
5. Lists available files.

Functions:
- validateApiKey(apiKey): Validates the API key format.
- connectToOpenAI(apiKey): Connects to the OpenAI API and performs connectivity and rate limit checks.
- listModels(): Lists all available models.
- checkMissingModels(availableModels): Checks for missing required models.
- listFiles(apiKey): Lists all available files.

Note: This utility requires the `openai` and `requests` libraries to be installed.
"""

import openai
import os
import sys
import requests

# Define constant API key
API_KEY = "your-api-key"

# Define hard-coded models of interest for exception reporting
HARDCODED_MODELS = [
    "text-davinci-002",
    "code-davinci-002",
    "text-davinci-003",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314"
]

def validateApiKey(apiKey):
    """
    Validate the API key.

    Parameters:
    - apiKey (str): The API key to validate.

    Raises:
    - SystemExit: If the API key is missing or invalid.

    Returns:
    - None

    """
    if not apiKey:
        print("No API key provided.")
        sys.exit(1)
    if not apiKey.startswith('sk-'):
        print("Invalid API key.")
        sys.exit(1)
    else:
        print("API key validation successful.")

def connectToOpenAI(apiKey):
    """
    Connect to the OpenAI API.

    Parameters:
    - apiKey (str): The API key to connect with.

    Raises:
    - SystemExit: If there is an error connecting to the API or if authentication/authorization fails.

    Returns:
    - None

    """
    try:
        openai.api_key = apiKey
        # Check connectivity to OpenAI API gateway
        response = requests.get("https://api.openai.com")
        if response.text.strip():
            print("Successfully connected to OpenAI API.")
        else:
            print("Failed to connect to OpenAI. Empty response received.")
            sys.exit(1)

        # Check for rate limit exceeded error
        if "Retry-After" in response.headers:
            retry_after = int(response.headers["Retry-After"])
            print(f"API rate limit exceeded. Retry after {retry_after} seconds.")
            sys.exit(1)

        # Rest of the code for API connection and model listing...
        models = listModels()

    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to OpenAI: {str(e)}")
        sys.exit(1)
    except openai.error.AuthenticationError:
        print("Authentication failed. Please check your API key.")
        sys.exit(1)
    except openai.error.AuthorizationError:
        print("Authorization failed. Please check your permissions.")
        sys.exit(1)

def listModels():
    """
    List all available models.

    This function connects to the OpenAI API and retrieves a list of all available models.
    It prints the list of models in alphabetical order.

    Returns:
        availableModels (list): A list of available model IDs.

    Raises:
        openai.error.AuthenticationError: If the API key authentication fails.
        openai.error.AuthorizationError: If the API key authorization fails.
        openai.error.RateLimitError: If the API rate limit is exceeded.
        Exception: For any other error encountered while listing models.
    """
    try:
        models = openai.Model.list()
        availableModels = sorted([model.id for model in models["data"]])
        for model in availableModels:
            print(f"- {model}")
        return availableModels
    except openai.error.AuthenticationError:
        print("Authentication failed. Please check your API key.")
        sys.exit(1)
    except openai.error.AuthorizationError:
        print("Authorization failed. Please check your permissions.")
        sys.exit(1)
    except openai.error.RateLimitError as e:
        retry_after = e.response.headers.get("Retry-After")
        if retry_after:
            print(f"API rate limit exceeded. Retry after {retry_after} seconds.")
        else:
            print("API rate limit exceeded.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to list models: {e}")
        sys.exit(1)

def checkMissingModels(availableModels):
    """
    Check for missing models in the required list.

    This function compares the available models with a list of required models,
    and prints any missing models that are not accessible.

    Args:
        availableModels (list): A list of available model IDs.

    Returns:
        None

    Prints:
        Missing models: If any models are missing and not accessible.
        Access to all required models: If all required models are accessible.
    """
    requiredModels = []

    # Check if oaimodellist.txt exists and is not empty
    if os.path.isfile("oaimodellist.txt"):
        with open("oaimodellist.txt", "r") as file:
            requiredModels = [line.strip() for line in file if line.strip()]
    else:
        requiredModels = HARDCODED_MODELS

    missingModels = [model for model in requiredModels if model not in availableModels]

    if missingModels:
        print("\nMissing models:")
        for model in missingModels:
            print(f"- {model}")
    else:
        print("\nAccess to all required models.")

def listFiles(apiKey):
    """
    List all files available to the user.

    This function retrieves a list of all files available to the user associated with the provided API key.
    It makes a GET request to the OpenAI API's `/v1/files` endpoint and prints the IDs of the files.

    Args:
        apiKey (str): The OpenAI API key.

    Returns:
        None

    Prints:
        Files available to the user: IDs of the files, or "None" if no files are available.
    """
    try:
        url = "https://api.openai.com/v1/files"
        headers = {"Authorization": f"Bearer {apiKey}"}
        response = requests.get(url, headers=headers)
        files = response.json()["data"]

        print("\nFiles available to you:")
        if len(files) == 0:
            print("None")
        else:
            for file in files:
                print(f"- {file['id']}")

        # Debug print for full response
        filesDebug = response.json()
#        print("--->> START File Debug Print")
#        print(filesDebug)
#        print(" END File Debug Print<<---")
    except Exception as e:
        print(f"Failed to list files: {e}")

def main():
    """
    Main function to run the OpenAI API Key Checker.

    This function serves as the entry point of the program. It validates the API key, connects to the OpenAI API,
    lists all available models, checks for missing models, and lists all available files.

    Args:
        None

    Returns:
        None

    Prints:
        - API key validation status
        - Connection status with the OpenAI API
        - List of available models
        - List of missing models (if any)
        - List of available files

    Exits:
        The program exits if any critical errors occur during API key validation, API connection,
        model listing, or file listing.
    """
    # Check if API key is passed as an argument
    apiKey = sys.argv[1] if len(sys.argv) > 1 else API_KEY if API_KEY else os.getenv('OPENAI_API_KEY')

    # Validate API key
    validateApiKey(apiKey)

    # Connect to OpenAI API
    connectToOpenAI(apiKey)

    # List all models
    availableModels = listModels()

    # Check for missing models
    checkMissingModels(availableModels)

    # List all files
    listFiles(apiKey)

if __name__ == "__main__":
    main()
