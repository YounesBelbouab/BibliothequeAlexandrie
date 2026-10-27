"""Règles métier de l'inscription : validation puis enregistrement de l'adhérent."""

import hashlib
import re

import base_de_donnees

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MOT_DE_PASSE_LONGUEUR_MIN = 8
DOMAINE_ECOLE = "ecole.fr"


def valider_inscription(email: str, mot_de_passe: str) -> list[str]:
    """Retourne la liste des erreurs de saisie (vide si tout est valide)."""
    erreurs = []
    if not email:
        erreurs.append("L'e-mail est obligatoire.")
    elif not EMAIL_REGEX.match(email):
        erreurs.append("L'e-mail n'est pas valide.")
    elif not email.endswith("@" + DOMAINE_ECOLE):
        erreurs.append(f"L'e-mail doit appartenir au domaine @{DOMAINE_ECOLE}.")
    elif base_de_donnees.email_existe(email):
        erreurs.append("Un compte existe déjà avec cet e-mail.")
    if len(mot_de_passe) < MOT_DE_PASSE_LONGUEUR_MIN:
        erreurs.append(
            f"Le mot de passe doit contenir au moins {MOT_DE_PASSE_LONGUEUR_MIN} caractères."
        )
    return erreurs


def inscrire_adherent(email: str, mot_de_passe: str) -> list[str]:
    """Enregistre l'adhérent si la saisie est valide ; retourne les erreurs sinon."""
    email = email.lower()
    erreurs = valider_inscription(email, mot_de_passe)
    if not erreurs:
        hash_mot_de_passe = hashlib.sha256(mot_de_passe.encode("utf-8")).hexdigest()
        base_de_donnees.inserer_adherent(email, hash_mot_de_passe)
    return erreurs
