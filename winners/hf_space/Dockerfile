# Use a lightweight Python base image (fits the 2 vCPU / 8GB RAM limit)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Install the environment in editable mode
RUN pip install -e .

# Expose the port for Gradio
EXPOSE 7860

# Set environment variables for Gradio
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# The default command runs the Gradio app for HF Spaces
# For inference, judges will override with: python inference.py
CMD ["python", "app.py"]