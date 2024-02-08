FROM python:3.12

# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

# Set the working directory
WORKDIR /app

# Install PostgreSQL client, gcc, libpq-dev (PostgreSQL dev), cmake, and wget (for downloading dockerize)
RUN apt-get update && \
    apt-get install -y postgresql-client gcc libpq-dev cmake wget && \
    # Install dockerize
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy the poetry dependencies before installing
COPY pyproject.toml poetry.lock* /app/

# Install poetry dependencies
RUN poetry install

# Copy all files to the app dir (workdir)
COPY . .

# Expose the port
EXPOSE 8050

# Use dockerize to wait for the fastapi service to be ready before starting the dash app
CMD ["dockerize", "-wait", "tcp://fastapi:5000", "-timeout", "60s", "python", "dashboard/app.py"]





 