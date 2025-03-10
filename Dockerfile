# 1. Basis-Image (Python 3.10-slim als Beispiel)
FROM python:3.10-slim

# 2. Setze das Arbeitsverzeichnis
WORKDIR /app

# 3. Kopiere die requirements.txt ins Image
COPY requirements.txt .

# 4. Installiere benötigte Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiere den Rest des Projektverzeichnisses ins Image
COPY . .

# 6. Exponiere den Port (für lokale Tests oder Dokumentation)
# (Streamlit läuft standardmäßig auf 8501)
EXPOSE 8501

# 7. Definiere den Container-Startbefehl
# Hinweis: Manche Cloud-Anbieter (z. B. Azure App Service) übergeben den Port als Umgebungsvariable $PORT.
# Um das abzufangen, kannst du folgendes Kommando verwenden:
CMD ["sh", "-c", "streamlit run ai_initiative_evaluation_vModular.py --server.port=8501 --server.address=0.0.0.0"]
