# # --- Step 1: Add Ollama as a Python dependency ---
# print("--- Installing the 'ollama' python package... ---")
# # LangChain uses this library to communicate with the Ollama service
# !uv pip install ollama
#
# # --- Step 2: Update the requirements.txt file ---
# print("\n--- Updating requirements.txt... ---")
# !uv pip freeze > requirements.txt
# print("requirements.txt has been updated.")

# --- Step 3: Install and run the Ollama service ---
print("\n--- Installing and running the Ollama service... ---")
# Install Ollama using the official script
!curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama as a background process
import subprocess
import time

command = "ollama serve"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("--- Starting Ollama... (please wait a moment) ---")
time.sleep(5) # Give it a moment to start

# Pull the Llama 3 model
!ollama pull llama3
print("\n--- Ollama is running and Llama 3 is ready! ---")