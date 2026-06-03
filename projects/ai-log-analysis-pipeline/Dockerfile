FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --shell /usr/sbin/nologin appuser

COPY analyzer.py .

USER appuser
EXPOSE 8383
CMD ["uvicorn", "analyzer:app", "--host", "0.0.0.0", "--port", "8383"]
