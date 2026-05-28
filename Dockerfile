# Use a builder stage with uv
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app

# Enable bytecode compilation for performance and startup speed
ENV UV_COMPILE_BYTECODE=1

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install dependencies (creates a virtualenv inside /app/.venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Use a lightweight runner stage
FROM python:3.13-alpine

WORKDIR /app

# Copy virtualenv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure we use the virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY run.py ./
COPY app ./app

# Expose port
EXPOSE 5001

# Set production settings
ENV FLASK_ENV=production
ENV PORT=5001

# Run the app
CMD ["python", "run.py"]
