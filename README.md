🎓 HelloAsso Checkout – Projet python

Ce projet met en place un serveur python permettant à une association étudiante de gérer des paiements via l’API HelloAsso (sandbox ou production).
L’interface web simple (HTML/CSS/JS) permet à l’utilisateur de remplir un formulaire d’adhésion et de lancer un paiement par carte bancaire.

Fichier .env
PORT=3000
HELLOASSO_CLIENT_ID=ton_client_id
HELLOASSO_CLIENT_SECRET=ton_client_secret
HELLOASSO_API_URL=https://api.helloasso-sandbox.com

Lancement du serveur
En local : 
cd helloasso-python-backend
source .venv/bin/activate
uvicorn main:app --reload --port 5000
En ligne: https://fai-checkout.onrender.com

💳 Fonctionnement du paiement HelloAsso
L’utilisateur clique sur le bouton depuis index.html pour accéder au formulaire.html.
Le formulaire envoie les données (nom, email, etc.) au backend python (/api/helloasso/create-payment).
Le serveur :
    récupère un token d’accès OAuth2 via ton client_id / client_secret
    envoie la requête de création de paiement à HelloAsso
    HelloAsso renvoie les infos du paiement (URL de checkout, statut, etc.)
    Tu peux ensuite rediriger ton utilisateur vers cette page de paiement.

Technologies utilisées
| Catégorie        | Outil                             |
| ---------------- | --------------------------------- |
| Backend          | Python (FastApi)               |
| API externe      | HelloAsso                         |
| Frontend         | HTML, CSS, JavaScript             |
| Authentification | OAuth2 (Client Credentials)       |
| Environnement    | dotenv                            |
| CORS             | Gestion des requêtes cross-origin |
| Déploiement      | Render / Railway / Vercel         |
