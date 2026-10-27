"""Accès à la base SQLite des adhérents."""

import sqlite3
from pathlib import Path

CHEMIN_BD = Path(__file__).resolve().parents[2] / "bibliotheque.db"


def connecter() -> sqlite3.Connection:
    connexion = sqlite3.connect(CHEMIN_BD)
    connexion.execute(
        """CREATE TABLE IF NOT EXISTS adherent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            hash_mot_de_passe TEXT NOT NULL
        )"""
    )
    return connexion


def email_existe(email: str) -> bool:
    with connecter() as connexion:
        ligne = connexion.execute(
            "SELECT 1 FROM adherent WHERE email = ?", (email,)
        ).fetchone()
    return ligne is not None


def inserer_adherent(email: str, hash_mot_de_passe: str) -> None:
    with connecter() as connexion:
        connexion.execute(
            "INSERT INTO adherent (email, hash_mot_de_passe) VALUES (?, ?)",
            (email, hash_mot_de_passe),
        )
