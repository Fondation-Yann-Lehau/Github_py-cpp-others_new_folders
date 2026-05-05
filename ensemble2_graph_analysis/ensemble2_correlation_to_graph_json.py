#!/usr/bin/env python3
"""
Analyse un dossier de .txt/.md et produit un graphe JSON (nodes/edges)
basé sur la similarité cosinus, inspiré de tes scripts "01-05-2026".

Sortie: correlation_graph.json (dans le même dossier que ce script)
"""

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


STOPWORDS = {
    "les", "des", "une", "est", "pour", "dans", "sur", "qui", "que", "avec", "par", "pas", "plus",
    "vous", "nous", "ils", "elles",
    "import", "return", "class", "const", "classname", "function", "def",
}

WORD_RE = re.compile(r"\b\w{3,}\b", re.UNICODE)


def tokenize(text: str) -> List[str]:
    words = [w.lower() for w in WORD_RE.findall(text)]
    return [w for w in words if w not in STOPWORDS]


def cosine_similarity(a: str, b: str) -> float:
    va = Counter(tokenize(a))
    vb = Counter(tokenize(b))
    inter = set(va) & set(vb)
    num = sum(va[x] * vb[x] for x in inter)
    da = math.sqrt(sum(v * v for v in va.values()))
    db = math.sqrt(sum(v * v for v in vb.values()))
    if da == 0 or db == 0:
        return 0.0
    return float(num) / (da * db)


@dataclass
class Doc:
    name: str
    text: str


def load_docs(folder: Path) -> List[Doc]:
    docs: List[Doc] = []
    for entry in sorted(folder.iterdir()):
        if entry.is_file() and entry.suffix.lower() in {".txt", ".md"}:
            try:
                docs.append(Doc(entry.name, entry.read_text(encoding="utf-8", errors="replace")))
            except Exception:
                continue
    return docs


def build_graph(docs: List[Doc], threshold_percent: float = 2.0) -> Dict:
    nodes = []
    edges = []

    for d in docs:
        nodes.append({
            "id": d.name,
            "label": d.name,
            "group": "document",
            "value": 20,
        })

    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            score = cosine_similarity(docs[i].text, docs[j].text)
            pct = round(score * 100, 2)
            if pct >= threshold_percent:
                edges.append({
                    "from": docs[i].name,
                    "to": docs[j].name,
                    "value": max(1.0, score * 10.0),
                    "title": f"Similarité: {pct}%",
                    "percent": pct,
                })

    return {"nodes": nodes, "edges": edges}


def main():
    # On analyse le dossier PARENT du script (pratique quand tu l'exécutes depuis ailleurs)
    script_dir = Path(__file__).resolve().parent

    docs = load_docs(script_dir)
    if not docs:
        raise SystemExit("Aucun .txt/.md trouvé dans le dossier du script.")

    graph = build_graph(docs, threshold_percent=2.0)

    out = script_dir / "correlation_graph.json"
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK -> {out}")
    print(f"nodes={len(graph['nodes'])}, edges={len(graph['edges'])}")


if __name__ == "__main__":
    main()
