# Base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1  # uv installs into system python

# Install curl (needed to fetch uv)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv (single binary)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set workdir to project root
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen --no-cache

# Copy the rest of the code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Workdir to src (since you run streamlit inside it)
WORKDIR /app/src

# Run Streamlit
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
