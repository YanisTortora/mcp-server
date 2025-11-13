FROM python:3.11-slim

# Déps système utiles (certifs, build basique)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Déps Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY app.py tools.py ./

EXPOSE 8787
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8787"]
