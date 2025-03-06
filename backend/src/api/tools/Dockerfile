# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
# WORKDIR /api

# ENV PYTHONPATH=/api

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY ../../pyproject.toml ../../poetry.lock ./

COPY . .
# Install the dependencies
RUN poetry install

# Copy the FastAPI application code into the container

# Expose the FastAPI port
EXPOSE 8001

# Run the FastAPI application
CMD ["/api/entrypoint.sh"]