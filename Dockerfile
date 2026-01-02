FROM python:3.12-slim

WORKDIR /app

COPY scripts/ scripts/
COPY lineups/ lineups/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scripts/generator.py"]
