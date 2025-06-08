FROM python:3.11-slim

# Crée un dossier pour ton app
WORKDIR /app

# Copie les dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY . .

CMD ["python", "app/main.py"]
