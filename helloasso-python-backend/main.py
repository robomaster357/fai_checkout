from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv

# 🔐 Charger les variables d'environnement
load_dotenv()

app = FastAPI()

# Servir le dossier contenant ton HTML et CSS
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_form():
    """Renvoie ton formulaire HTML"""
    return FileResponse("static/formulaire.html")


@app.post("/api/helloasso/create-payment")
async def create_payment(request: Request):
    """Reproduit ton helloassoRoutes.js en Python"""
    try:
        body = await request.json()
        first_name = body.get("firstName")
        last_name = body.get("lastName")
        email = body.get("email")
        amount = int(float(body.get("amount", 0)) * 100)  # euros → centimes

        async with httpx.AsyncClient() as client:
            # 1️⃣ Obtenir le token HelloAsso
            token_resp = await client.post(
                f"{os.getenv('HELLOASSO_API_URL')}/oauth2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": os.getenv("HELLOASSO_CLIENT_ID"),
                    "client_secret": os.getenv("HELLOASSO_CLIENT_SECRET"),
                },
            )

            if token_resp.status_code != 200:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Erreur récupération token",
                        "details": token_resp.text,
                    },
                )

            token = token_resp.json()["access_token"]

            # 2️⃣ Construire le JSON du paiement
            payment_data = {
                "totalAmount": amount,
                "initialAmount": amount,
                "itemName": "Box fibre",
                "backUrl": "https://fai-checkout.onrender.com/back",
                "errorUrl": "https://fai-checkout.onrender.com/error",
                "returnUrl": "https://fai-checkout.onrender.com/return",
                "containsDonation": False,
                "payer": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "dateOfBirth": "1986-07-06",
                    "address": "23 rue du palmier",
                    "city": "Paris",
                    "zipCode": "75000",
                    "country": "FRA",
                    "companyName": "HelloAsso",
                },
                "metadata": {
                    "reference": 12345,
                    "libelle": "Adhesion Football",
                    "userId": 98765,
                    "produits": [
                        {"id": 56, "count": 1},
                        {"id": 78, "count": 3},
                    ],
                },
            }

            # 3️⃣ Création du checkout HelloAsso
            checkout_resp = await client.post(
                f"{os.getenv('HELLOASSO_API_URL')}/v5/organizations/{os.getenv('ORG_SLUG')}/checkout-intents",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payment_data,
            )

            if checkout_resp.status_code != 200:
                return JSONResponse(
                    status_code=checkout_resp.status_code,
                    content={
                        "error": "Erreur création paiement HelloAsso",
                        "details": checkout_resp.text,
                    },
                )

            return checkout_resp.json()

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": "Erreur serveur HelloAsso", "details": str(e)}
        )
