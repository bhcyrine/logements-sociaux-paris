# Logements sociaux à Paris : Mode de réalisation et niveau de "socialité"

## Le sujet en une phrase

Est-ce que la façon dont un logement social est produit (construit neuf, rénové, ou racheté déjà existant) change le type de logement qu'on obtient au final ?


## L'hypothèse

Le mode de réalisation d'un programme de logement social détermine sa composition 
en types de financement. En particulier, l'acquisition-conventionnement (rachat de 
logements existants) produit une proportion de logements très sociaux (PLA I) 
nettement plus faible que la construction neuve ou l'acquisition-réhabilitation, 
au profit des logements PLS (intermédiaires).

## Le résultat, en une phrase

**Confirmé.** Les logements rachetés existants contiennent 15,9% de PLA I, contre 18,1% en construction neuve et 26,1% en rénovation. L'écart est confirmé statistiquement (intervalle de confiance à 95%), stable sur 20 ans, et présent dans 15 des 20 arrondissements de Paris.

## D'où viennent les données

Fichier "Logements sociaux financés à Paris" : Open Data Paris (https://opendata.paris.fr).
4 174 programmes de logement social, 126 547 logements au total, de 2001 à 2024.

Récupéré via l'API Explore 2.1 de la Ville de Paris (`src/api.py`), plutôt qu'en téléchargement manuel :

```python
from src.api import download_dataset
df = download_dataset()  # télécharge et sauvegarde dans data/raw/
```

## Comment le projet est organisé

```
data/
  raw/          → le fichier téléchargé, tel quel
  processed/    → le fichier après nettoyage (produit par 02)
notebooks/
  01_data_understanding.ipynb   → exploration des données, recherche d'anomalies
  02_data_cleaning.ipynb        → nettoyage, à partir des décisions prises en 01
  03_analysis.ipynb             → calculs, graphiques, et conclusion finale
src/
  api.py        → récupération du dataset via l'API Open Data Paris
outputs/        → tous les graphiques générés (images .png)
```

## Comment relancer le projet

1. Récupérer les données : exécuter `src/api.py` (ou utiliser `download_dataset()`), ou utiliser directement le fichier déjà présent dans `data/raw/`.
2. Ouvrir et exécuter les notebooks **dans l'ordre** : `01` → `02` → `03`. Chaque notebook charge le fichier produit par le précédent.

*(Les notebooks chargent directement le fichier CSV présent dans `data/raw/` et `src/api.py` sert à le récupérer ou l'actualiser depuis la source, mais n'est pas appelé automatiquement par les notebooks.)*

Packages nécessaires : `pandas`, `numpy`, `matplotlib`, `statsmodels`, `requests`.

```
pip install pandas numpy matplotlib statsmodels requests
```

## Les 3 décisions méthodologiques clés

1. **Pourquoi filtrer sur "logement familial" (85% des données) ?**
   Les résidences spécialisées (étudiants, personnes âgées...) suivent presque toujours le même mode de réalisation. Les inclure aurait faussé la comparaison , on comparerait des populations différentes, pas juste des méthodes de construction.

2. **Pourquoi retenir 1,4x plutôt que 2,2x (chiffre sans filtre) ?**
   Le chiffre plus élevé (2,2x) est gonflé par les résidences spécialisées. Le 1,4x, calculé sur le logement familial uniquement, est la mesure la plus fiable pour caractériser le logement social "classique" , ce choix est documenté plutôt que masqué.

3. **Est-ce que le mode de réalisation cause la différence ?**
   Non : l'analyse montre une association statistique solide, pas un lien de cause à effet. D'autres facteurs (contexte foncier, politique locale) peuvent expliquer une partie de l'écart , voir la section "Limites" du notebook 03.

## Ce que contient ce dépôt

- **`notebooks/01, 02, 03`** - tout le travail d'analyse : exploration, nettoyage, puis calculs et graphiques. Chaque étape est expliquée en markdown avant le code.
- **`src/api.py`** — récupération du dataset via l'API Open Data Paris.
- **`outputs/`** — tous les graphiques générés, en image.
