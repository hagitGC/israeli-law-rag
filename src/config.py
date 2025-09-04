# This file is responsible for loading environment variables for the project.
import os
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root
# find_dotenv() will search for the .env file in parent directories
from dotenv import find_dotenv
load_dotenv(find_dotenv())

# Example of how to get an API key.
# We will use this later when we connect to an LLM.
# To use it, you would add OPENAI_API_KEY="your_key_here" to your .env file.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# You can add other configurations here as the project grows.