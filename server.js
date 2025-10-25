// server.js
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import cors from "cors";
import helloassoRoutes from "./routes/helloassoRoutes.js";
import open from "open";

// 🧩 Configuration de base
dotenv.config();

const app = express();
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3000;

// 🔧 Middlewares
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // Sert les fichiers HTML/CSS/JS

// 🧭 Routes API
app.use("/api/helloasso", helloassoRoutes);

// 🏠 Route d'accueil
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 🚀 Lancement du serveur
app.listen(PORT, () => {
  console.log(`✅ Serveur lancé sur http://localhost:${PORT}`);
  //open(`http://localhost:${PORT}`);
});

