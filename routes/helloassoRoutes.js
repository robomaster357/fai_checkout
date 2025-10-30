// routes/helloassoRoutes.js
import express from "express";
import fetch from "node-fetch";

const router = express.Router();

// Exemple : route pour créer un paiement HelloAsso
router.post("/create-payment", async (req, res) => {
  try {
    // 🔐 Récupération du token HelloAsso
    const tokenResponse = await fetch(`${process.env.HELLOASSO_API_URL}/oauth2/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        client_id: process.env.HELLOASSO_CLIENT_ID,
        client_secret: process.env.HELLOASSO_CLIENT_SECRET,
      }),
    });

    if (!tokenResponse.ok) {
      const text = await tokenResponse.text();
      console.error("❌ Erreur token HelloAsso:", text);
      return res.status(400).json({ error: "Erreur récupération token", details: text });
    }

    const tokenData = await tokenResponse.json();
    console.log(tokenData)

    // 🧩 Données reçues du formulaire
    const { firstName, lastName, email, amount } = req.body;

    //Formattage du json à envoyer à l'API
    const paymentData = {
        totalAmount: 20*100, //en centimes
        initialAmount: 20*100,
        itemName: "Box fibre",
        backUrl: "https://fai-checkout.onrender.com/cancel",
        errorUrl: "https://fai-checkout.onrender.com/error",
        returnUrl: "https://fai-checkout.onrender.com/return",
        containsDonation: false,
        payer: {
            firstName: firstName,
            lastName: lastName,
            email: email,
            companyName: "HelloAsso"
        },
        };

    // 💳 Création du checkout (paiement)
    const checkoutResponse = await fetch(
      `${process.env.HELLOASSO_API_URL}/v5/organizations/${process.env.ORG_SLUG}/checkout-intents`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${tokenData.access_token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(paymentData),
      }
    );

    // Lire la réponse brute immédiatement
    const text = await checkoutResponse.text();

    // ✅ Vérifier le statut HTTP
    if (!checkoutResponse.ok) {
      console.error("❌ Erreur création paiement HelloAsso:", text);
      return res.status(checkoutResponse.status).json({
        error: "Erreur création paiement HelloAsso",
        details: text,
      });
    }

    // ✅ Puis seulement parser en JSON
    let checkoutData;
    try {
      checkoutData = JSON.parse(text); // tenter de parser JSON
    } catch (err) {
      console.error("❌ Impossible de parser la réponse JSON:", text);
      return res.status(500).json({
        error: "Réponse HelloAsso invalide",
        details: text,
      });
    }

    res.json(checkoutData);
  } catch (err) {
    console.error("Erreur lors de la création du paiement HelloAsso:", err);
    res.status(500).json({ error: "Erreur serveur HelloAsso" });
  }
});

export default router;
