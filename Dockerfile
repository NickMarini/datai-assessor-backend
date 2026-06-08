# Use a lightweight Python base image
FROM python:3.11-slim-bookworm

# Set the working directory
WORKDIR /app

# Install uv directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the uv configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies into the system environment to keep the container lightweight
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the application code
COPY ./app ./app

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]