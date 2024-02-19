FROM python:3.12

# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install PostgreSQL client, gcc, libpq-dev (PostgreSQL dev), and cmake
RUN apt-get update && \
    apt-get install -y postgresql-client gcc libpq-dev cmake && \
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
EXPOSE 5000



CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]





 