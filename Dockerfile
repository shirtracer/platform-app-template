# syntax=docker/dockerfile:1
# Example app image. Pin the base image by digest; secrets never go into the image (the
# platform mounts them under /run/secrets/ at runtime).
FROM python:3.14.7-slim-trixie@sha256:51dafde81dbdb6ebde285137a295cf18a47ca95234fe388a343719cb97305b3d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY app/ /app/

USER 10001
EXPOSE 8080
CMD ["python", "/app/main.py"]
