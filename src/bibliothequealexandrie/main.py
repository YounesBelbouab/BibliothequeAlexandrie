"""Serveur de la Bibliothèque d'Alexandrie : sert le front et reçoit les inscriptions."""

import json
import re
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DOSSIER_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MOT_DE_PASSE_LONGUEUR_MIN = 8


def valider_inscription(email: str, mot_de_passe: str) -> list[str]:
    """Retourne la liste des erreurs de saisie (vide si tout est valide)."""
    erreurs = []
    if not email:
        erreurs.append("L'e-mail est obligatoire.")
    elif not EMAIL_REGEX.match(email):
        erreurs.append("L'e-mail n'est pas valide.")
    if len(mot_de_passe) < MOT_DE_PASSE_LONGUEUR_MIN:
        erreurs.append(
            f"Le mot de passe doit contenir au moins {MOT_DE_PASSE_LONGUEUR_MIN} caractères."
        )
    return erreurs


class Gestionnaire(SimpleHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/api/inscription":
            self.send_error(404)
            return

        try:
            longueur = int(self.headers.get("Content-Length", 0))
            donnees = json.loads(self.rfile.read(longueur))
            email = str(donnees.get("email", "")).strip()
            mot_de_passe = str(donnees.get("motDePasse", ""))
        except (ValueError, AttributeError):
            self._repondre(400, {"erreurs": ["Requête invalide."]})
            return

        erreurs = valider_inscription(email, mot_de_passe)
        if erreurs:
            self._repondre(400, {"erreurs": erreurs})
            return

        self._repondre(201, {"message": f"Compte créé pour {email} !"})

    def _repondre(self, statut: int, corps: dict) -> None:
        contenu = json.dumps(corps).encode("utf-8")
        self.send_response(statut)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(contenu)))
        self.end_headers()
        self.wfile.write(contenu)


def main(port: int = 8000) -> None:
    gestionnaire = partial(Gestionnaire, directory=str(DOSSIER_FRONTEND))
    serveur = HTTPServer(("127.0.0.1", port), gestionnaire)
    print(f"Serveur lancé sur http://127.0.0.1:{port}")
    serveur.serve_forever()


if __name__ == "__main__":
    main()
