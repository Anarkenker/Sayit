FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md README.zh-CN.md LICENSE ./
COPY src ./src

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir .

ENTRYPOINT ["sayit"]
