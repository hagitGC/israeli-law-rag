# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt .
# We use --no-cache-dir to keep the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the application source code and the vector store
COPY ./src ./src
COPY ./vectorstores ./vectorstores

# Step 5: Expose the port the app will run on
EXPOSE 8000

# Step 6: Define the command to run the application using uvicorn
# This will start the FastAPI server
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
