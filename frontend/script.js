const EMAIL_REGEX = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const MOT_DE_PASSE_LONGUEUR_MIN = 8;

const formulaire = document.getElementById("formulaire-inscription");
const champEmail = document.getElementById("email");
const champMdp = document.getElementById("mot-de-passe");
const caseAfficherMdp = document.getElementById("afficher-mdp");
const erreurEmail = document.getElementById("erreur-email");
const erreurMdp = document.getElementById("erreur-mot-de-passe");
const messageSucces = document.getElementById("message-succes");

function validerEmail(email) {
  if (!email) return "L'e-mail est obligatoire.";
  if (!EMAIL_REGEX.test(email)) return "L'e-mail n'est pas valide.";
  return "";
}

function validerMotDePasse(motDePasse) {
  if (motDePasse.length < MOT_DE_PASSE_LONGUEUR_MIN) {
    return `Le mot de passe doit contenir au moins ${MOT_DE_PASSE_LONGUEUR_MIN} caractères.`;
  }
  return "";
}

function afficherErreur(champ, zone, message) {
  zone.textContent = message;
  champ.classList.toggle("invalide", message !== "");
}

caseAfficherMdp.addEventListener("change", () => {
  champMdp.type = caseAfficherMdp.checked ? "text" : "password";
});

formulaire.addEventListener("submit", async (event) => {
  event.preventDefault();
  messageSucces.textContent = "";

  const email = champEmail.value.trim();
  const motDePasse = champMdp.value;

  const msgEmail = validerEmail(email);
  const msgMdp = validerMotDePasse(motDePasse);
  afficherErreur(champEmail, erreurEmail, msgEmail);
  afficherErreur(champMdp, erreurMdp, msgMdp);

  if (msgEmail || msgMdp) return;

  try {
    const reponse = await fetch("/api/inscription", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, motDePasse }),
    });
    const resultat = await reponse.json();

    if (!reponse.ok) {
      afficherErreur(champEmail, erreurEmail, resultat.erreurs.join(" "));
      return;
    }
    messageSucces.textContent = resultat.message;
    champMdp.value = "";
  } catch {
    afficherErreur(champEmail, erreurEmail, "Impossible de joindre le serveur.");
  }
});
