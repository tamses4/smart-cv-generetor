#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse automatique du code Python du projet Smart CV Generator.
Vérifie le formatage (Black), le style (Flake8) et le typage (Mypy).
Les résultats sont affichés clairement et peuvent être enrichis par l'IA plus tard.
"""

import subprocess
import sys
import io
import os
from typing import Tuple
from dotenv import load_dotenv

# Forcer l'encodage UTF-8 sur Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Charger les variables locales (.env) si présentes
load_dotenv()

# Récupération des secrets via les variables d'environnement définies dans GitHub Actions
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

if not GEMINI_API_KEY:
    print("⚠️  Avertissement : aucune clé IA détectée. Définis GEMINI_API_KEY dans tes secrets GitHub ou ton .env.")
else:
    print("🔑 Clé API IA détectée (masquée pour sécurité).")

# --- Fonctions utilitaires ---

def run_command(command: str) -> Tuple[int, str]:
    """Exécute une commande shell et retourne (code_retour, sortie)."""
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.returncode, process.stdout + process.stderr

def print_status(tool: str, success: bool, details: str = "") -> None:
    """Affiche un message coloré selon le succès ou l’échec."""
    symbol = "✅" if success else "❌"
    print(f"{symbol} {tool} {'réussi' if success else 'a échoué.'}")
    if not success and details:
        print(details)
    print()

# --- Analyse principale ---

def main() -> None:
    print("🚀 Lancement de l'analyse du projet Smart CV Generator...\n")

    tools = {
        "Black (formatage)": "black --check app/",
        "Flake8 (lint)": "flake8 app/",
        "Mypy (typage strict)": "mypy app/"
    }

    global_success = True

    for tool, command in tools.items():
        print(f"🔍 {tool}...")
        code, output = run_command(command)
        success = code == 0
        print_status(tool, success, output.strip())
        if not success:
            global_success = False

    if not global_success:
        print("🚫 Des problèmes ont été détectés. Corrigez-les avant de committer/pusher.\n")
        sys.exit(1)

    print("🎉 Tout est propre ! Le code respecte les standards de qualité.\n")

if __name__ == "__main__":
    main()
