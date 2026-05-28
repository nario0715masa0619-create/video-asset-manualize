# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# - ffmpeg and ffprobe for video processing
# - fonts-noto-cjk for Japanese font rendering in PDF
# - build-essential for compiling python packages if necessary
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-noto-cjk \
    fontconfig \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install the application in editable mode
RUN pip install -e .

# Expose Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
