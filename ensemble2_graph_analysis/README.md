# Ensemble 2 — Corrélation Python / HTML / PHP + visualiseur HTML

## 1) Générer les exports de corrélation

Depuis ce dossier :

```bash
python3 ensemble2_correlation_to_graph_json.py
```

Cela crée :
- `correlation_graph.json` (graphe nodes/edges pour le visualiseur),
- `correlation_summary.json` (synthèse structurée),
- `correlation_summary.md` (synthèse lisible).

Le script scanne automatiquement le repository pour corréler les fichiers :
- `*.py`
- `*.html` / `*.htm`
- `*.php`

## 2) Ouvrir le visualiseur

Lance un serveur web à la racine du repo (ou ici) :

```bash
python3 -m http.server 8000
```

Puis ouvre :

- http://localhost:8000/ensemble2_graph_analysis/ensemble2_graph_viewer.html

## Notes

- Le HTML charge `./correlation_graph.json` (dans le même dossier).
- Si tu ajoutes/modifies des fichiers Python, HTML ou PHP dans le repository, relance le script Python.
