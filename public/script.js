// public/script.js

// 🧭 Fonction appelée quand la page est chargée
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  const messageBox = document.getElementById("messageBox");

  if (!form) return; // S'il n'y a pas de formulaire sur la page (ex: index.html), on ne fait rien

  // 🎯 Quand l’utilisateur soumet le formulaire
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Empêche le rechargement de la page

    // 🔄 Affiche un message de chargement
    displayMessage("⏳ Création du paiement en cours...", "info");

    try {
      // 📦 Récupération des données du formulaire
      const formData = Object.fromEntries(new FormData(form).entries());

      // 💳 Préparation du corps de la requête pour HelloAsso
      const paymentBody = {
        totalAmount: 7000,
        itemName: "Adhésion Football",
        backUrl: "https://www.partnertest.com/back.php",
        errorUrl: "https://www.partnertest.com/error.php",
        returnUrl: "https://www.partnertest.com/return.php",
        payer: {
          firstName: formData.firstName,
          lastName: formData.lastName,
          email: formData.email,
          city: formData.city || "Paris",
          zipCode: formData.zipCode || "75000",
          country: "FRA",
        },
        metadata: {
          libelle: "Adhésion Football",
          userId: Math.floor(Math.random() * 100000),
        },
      };

      // 📡 Envoi de la requête POST vers ton backend Express
      const response = await fetch("/api/helloasso/create-payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(paymentBody),
      });

      // 📬 Récupération de la réponse JSON
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Erreur de création du paiement");
      }

      console.log("✅ Paiement créé :", result);
      displayMessage("✅ Paiement créé avec succès ! Redirection en cours...", "success");

      // 🔀 Si HelloAsso renvoie une URL de redirection (checkout URL)
      if (result.redirectUrl) {
        setTimeout(() => {
          window.location.href = result.redirectUrl;
        }, 1500);
      }
    } catch (err) {
      console.error("❌ Erreur :", err);
      displayMessage("❌ " + err.message, "error");
    }
  });
});

// 🧱 Fonction utilitaire pour afficher un message dynamique
function displayMessage(text, type = "info") {
  let box = document.getElementById("messageBox");

  // Si la boîte n'existe pas encore, on la crée
  if (!box) {
    box = document.createElement("div");
    box.id = "messageBox";
    box.style.marginTop = "15px";
    box.style.padding = "10px";
    box.style.borderRadius = "8px";
    box.style.fontFamily = "sans-serif";
    box.style.fontSize = "1rem";
    box.style.textAlign = "center";
    document.body.appendChild(box);
  }

  // Couleurs selon le type
  switch (type) {
    case "success":
      box.style.backgroundColor = "#d4edda";
      box.style.color = "#155724";
      break;
    case "error":
      box.style.backgroundColor = "#f8d7da";
      box.style.color = "#721c24";
      break;
    default:
      box.style.backgroundColor = "#cce5ff";
      box.style.color = "#004085";
      break;
  }

  box.textContent = text;
}
