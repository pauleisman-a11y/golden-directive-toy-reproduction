# Pinned base image. Run with: docker build -t golden-directive-toys . && docker run --rm golden-directive-toys
# Note: the Docker path is provided for strangers with Docker. It was
# NOT built in the environment that prepared this repo (no Docker daemon
# there). The verified path is the native one in REPRODUCIBILITY.md.
FROM python:3.12.7-slim-bookworm
WORKDIR /app
COPY . /app
CMD ["bash", "reproduce.sh"]
