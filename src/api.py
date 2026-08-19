"""
src/api.py

Module de récupération du dataset "Programmes de logements sociaux
financés à Paris" via l'API Explore 2.1 de la Ville de Paris (méthode 1 - API).

Usage :
    from src.api import download_dataset
    df = download_dataset()
"""

import os
import requests
from io import StringIO
import pandas as pd

# --- Configuration ---
DATASET_ID = "logements-sociaux-finances-a-paris"
API_URL = f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/{DATASET_ID}/exports/csv"
PARAMS = {"delimiter": ";"}

# Chemin relatif à la racine du projet (src/api.py -> ../data/raw)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{DATASET_ID}.csv")


def download_dataset(save: bool = True) -> pd.DataFrame:
    """
    Télécharge le dataset des logements sociaux financés à Paris via l'API Paris Data.

    Args:
        save: si True, sauvegarde le CSV brut dans data/raw/.

    Returns:
        DataFrame pandas contenant l'intégralité du dataset.
    """
    print("Téléchargement en cours via l'API...")
    response = requests.get(API_URL, params=PARAMS, timeout=60)
    response.raise_for_status()

    if save:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)
        print(f"Fichier sauvegardé : {OUTPUT_FILE}")
        print(f"Taille : {len(response.content) / 1_000_000:.2f} Mo")

    df = pd.read_csv(StringIO(response.text), sep=";")
    print(f"Nombre de lignes  : {len(df)}")
    print(f"Nombre de colonnes: {len(df.columns)}")
    print("Colonnes :", list(df.columns))

    return df


def preview_records(limit: int = 5) -> None:
    """
    Affiche un aperçu rapide via l'endpoint 'records' (utile pour vérifier
    les noms de colonnes et le total_count sans tout télécharger).
    """
    url = f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/{DATASET_ID}/records"
    response = requests.get(url, params={"limit": limit}, timeout=30)
    response.raise_for_status()
    data = response.json()

    print(f"Nombre total de lignes disponibles : {data['total_count']}")
    print("\nColonnes disponibles :")
    for key in data["results"][0].keys():
        print(f"  - {key}")
    print("\nExemple d'enregistrement :")
    print(data["results"][0])


if __name__ == "__main__":
    download_dataset()