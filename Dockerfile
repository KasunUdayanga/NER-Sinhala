FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Label Studio
RUN pip install label-studio

# Expose the port Label Studio will run on
EXPOSE 8080

# Start Label Studio when the container runs
CMD ["label-studio", "start", "--host", "0.0.0.0", "--port", "8080"]
