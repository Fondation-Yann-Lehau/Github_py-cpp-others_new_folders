# Ensemble 2 — Analyse de similarité cosinus + visualiseur HTML

## 1) Générer le graphe JSON

Depuis ce dossier :

```bash
python3 ensemble2_correlation_to_graph_json.py
```

Cela crée : `correlation_graph.json`

## 2) Ouvrir le visualiseur

Lance un serveur web à la racine du repo (ou ici) :

```bash
python3 -m http.server 8000
```

Puis ouvre :

- http://localhost:8000/ensemble2_graph_analysis/ensemble2_graph_viewer.html

## Notes

- Le HTML charge `./correlation_graph.json` (dans le même dossier).
- Si tu ajoutes des fichiers `.txt` ou `.md` dans ce dossier, relance le script Python.
