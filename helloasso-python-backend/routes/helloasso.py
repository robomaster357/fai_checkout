# helloasso-python-backend/routes/helloasso.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
import requests  # HTTP client plus simple que fetch
from dotenv import load_dotenv

router = APIRouter()

# 🧭 Charger le .env (utile si exécuté directement)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "..", ".env"))

# 🔧 Variables d'environnement
HELLOASSO_API_URL = os.getenv("HELLOASSO_API_URL")
HELLOASSO_CLIENT_ID = os.getenv("HELLOASSO_CLIENT_ID")
HELLOASSO_CLIENT_SECRET = os.getenv("HELLOASSO_CLIENT_SECRET")
ORG_SLUG = os.getenv("ORG_SLUG")

@router.post("/create-payment")
async def create_payment(request: Request):
    print("📩 Requête reçue sur /api/helloasso/create-payment")
    try:
        # 📦 Récupération du body JSON
        body = await request.json()
        firstName = body.get("firstName")
        lastName = body.get("lastName")
        email = body.get("email")

        # 🔑 Étape 1 : Récupération du token HelloAsso
        token_url = f"{HELLOASSO_API_URL}/oauth2/token"
        token_payload = {
            "grant_type": "client_credentials",
            "client_id": HELLOASSO_CLIENT_ID,
            "client_secret": HELLOASSO_CLIENT_SECRET,
        }
        token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.post(token_url, data=token_payload, headers=token_headers)

        if not token_response.ok:
            return JSONResponse(
                status_code=token_response.status_code,
                content={"error": "Erreur récupération token", "details": token_response.text},
            )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        # 🧾 Étape 2 : Créer le paiement HelloAsso
        payment_data = {
            "totalAmount": 2000,
            "initialAmount": 2000,
            "itemName": "Box fibre",
            "backUrl": "https://fai-checkout.onrender.com/back",
            "errorUrl": "https://fai-checkout.onrender.com/error",
            "returnUrl": "https://fai-checkout.onrender.com/return",
            "containsDonation": False,
            "payer": {
                "firstName": firstName,
                "lastName": lastName,
                "email": email,
                "companyName": "HelloAsso"
            }
        }

        checkout_url = f"{HELLOASSO_API_URL}/v5/organizations/{ORG_SLUG}/checkout-intents"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        checkout_response = requests.post(checkout_url, json=payment_data, headers=headers)
        raw_text = checkout_response.text  # pour debug éventuel

        if not checkout_response.ok:
            return JSONResponse(
                status_code=checkout_response.status_code,
                content={"error": "Erreur création paiement HelloAsso", "details": raw_text},
            )

        try:
            checkout_data = checkout_response.json()
        except Exception:
            return JSONResponse(status_code=500, content={
                "error": "Réponse HelloAsso invalide",
                "details": raw_text
            })

        return checkout_data

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": "Erreur serveur HelloAsso",
            "details": str(e)
        })
