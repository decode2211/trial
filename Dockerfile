# Use a lightweight Python base image (fits the 2 vCPU / 8GB RAM limit)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install openenv

# Copy the rest of the project files
COPY . .

# Install the environment in editable mode
RUN pip install -e .

# The judges will likely override this command, but it's good practice to have a default
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]