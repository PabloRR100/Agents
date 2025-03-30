FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy and install deps
COPY pyproject.toml uv.lock ./
RUN uv pip install -r uv.lock --system

# Copy app code
COPY . .

# Make script executable
RUN chmod +x run_api.sh

ENTRYPOINT ["./run_api.sh"]
