FROM python:buster

# Set environment variables to keep Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./src ./src

# Create mount points for external data/models
RUN mkdir /data /models

# Switch to the source directory to run the app
WORKDIR /app/src
CMD ["python", "recommender_app.py"]