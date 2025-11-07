# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install PDM
RUN pip install --no-cache-dir pdm

# Copy dependency files
COPY pyproject.toml pdm.lock* ./

# Install dependencies using PDM
RUN pdm install --prod --no-lock --no-editable

# Copy application source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app/src
ENV MONGODB_URL=mongodb://mongodb:27017
ENV DATABASE_NAME=users_db

# Run the application
CMD ["pdm", "run", "uvicorn", "mongo_db_communication_libraries.main:app", "--host", "0.0.0.0", "--port", "8000"]
