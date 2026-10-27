"""Serveur de la Bibliothèque d'Alexandrie : sert le front et reçoit les inscriptions."""

import json
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from service import inscrire_adherent

DOSSIER_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"


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

        erreurs = inscrire_adherent(email, mot_de_passe)
        if erreurs:
            self._repondre(400, {"erreurs": erreurs})
            return

        self._repondre(201, {"message": f"Bienvenue {email}, vous êtes connecté !"})

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
