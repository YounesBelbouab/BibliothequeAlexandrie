const DELAI_SAISIE_MS = 250;

const formulaire = document.getElementById("formulaire-recherche");
const champRecherche = document.getElementById("recherche");
const statut = document.getElementById("statut");
const liste = document.getElementById("liste-adherents");

let minuteur;
let derniereRequete = 0;

function afficherAdherents(adherents) {
  liste.replaceChildren(
    ...adherents.map((adherent) => {
      const element = document.createElement("li");
      const nom = document.createElement("strong");
      nom.textContent = `${adherent.prenom} ${adherent.nom}`;
      const email = document.createElement("span");
      email.textContent = adherent.email;
      element.append(nom, email);
      return element;
    })
  );
}

async function rechercher(requete) {
  const numero = ++derniereRequete;

  if (!requete) {
    afficherAdherents([]);
    statut.textContent = "";
    return;
  }

  try {
    const reponse = await fetch(`/api/adherents?q=${encodeURIComponent(requete)}`);
    const resultat = await reponse.json();
    // Ignore les réponses arrivées après une recherche plus récente.
    if (numero !== derniereRequete) return;

    afficherAdherents(resultat.adherents);
    const total = resultat.adherents.length;
    statut.textContent = total === 0
      ? "Aucun adhérent trouvé."
      : `${total} adhérent${total > 1 ? "s" : ""} trouvé${total > 1 ? "s" : ""}.`;
  } catch {
    if (numero !== derniereRequete) return;
    afficherAdherents([]);
    statut.textContent = "Impossible de joindre le serveur.";
  }
}

champRecherche.addEventListener("input", () => {
  clearTimeout(minuteur);
  minuteur = setTimeout(() => rechercher(champRecherche.value.trim()), DELAI_SAISIE_MS);
});

formulaire.addEventListener("submit", (event) => {
  event.preventDefault();
  clearTimeout(minuteur);
  rechercher(champRecherche.value.trim());
});
