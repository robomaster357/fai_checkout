# helloasso-python-backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from dotenv import load_dotenv
import os

# 🧭 Définir le chemin de base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔐 Charger le .env situé dans le dossier parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# 🚀 Initialisation de l’app FastAPI
app = FastAPI(title="HelloAsso Python Backend")

# 📂 Monter le dossier public (pour les fichiers statiques)
PUBLIC_DIR = os.path.join(BASE_DIR, "../public")
print("🧭 Dossier statique servi depuis :", os.path.abspath(PUBLIC_DIR))
app.mount("/", StaticFiles(directory=os.path.abspath(PUBLIC_DIR), html=True), name="static")


# 🏠 Route principale -> index.html (bouton de paiement)
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse(os.path.join(BASE_DIR, "public", "index.html"))

# 📦 Importer la route HelloAsso
from routes.helloasso import router as helloasso_router
app.include_router(helloasso_router, prefix="/api/helloasso")
