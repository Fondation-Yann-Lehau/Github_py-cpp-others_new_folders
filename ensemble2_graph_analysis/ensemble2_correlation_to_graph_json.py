#!/usr/bin/env python3
"""
Analyse transverse Python/HTML/PHP du repository et génération de synthèses:
- correlation_graph.json (visualisation)
- correlation_summary.json (export structuré)
- correlation_summary.md (synthèse lisible)
"""

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple


STOPWORDS = {
    "les", "des", "une", "est", "pour", "dans", "sur", "qui", "que", "avec", "par", "pas", "plus",
    "vous", "nous", "ils", "elles",
    "import", "return", "class", "const", "classname", "function", "def", "include", "require",
    "script", "html", "php", "python",
}

WORD_RE = re.compile(r"\b\w{3,}\b", re.UNICODE)
REFERENCE_RE = re.compile(r"[\w/-]+\.(?:py|html?|php)\b", re.IGNORECASE)
LANGUAGE_BY_EXT = {
    ".py": "Python",
    ".html": "HTML",
    ".htm": "HTML",
    ".php": "PHP",
}


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
    path: str
    text: str
    language: str
    series: str


def detect_series(path: Path) -> str:
    return path.parts[0] if len(path.parts) > 1 else "root"


def load_docs(repo_root: Path) -> List[Doc]:
    docs: List[Doc] = []
    for entry in sorted(repo_root.rglob("*")):
        if (
            entry.is_file()
            and entry.suffix.lower() in LANGUAGE_BY_EXT
            and ".git" not in entry.parts
            and "__pycache__" not in entry.parts
        ):
            rel = entry.relative_to(repo_root)
            try:
                docs.append(
                    Doc(
                        path=rel.as_posix(),
                        text=entry.read_text(encoding="utf-8", errors="replace"),
                        language=LANGUAGE_BY_EXT[entry.suffix.lower()],
                        series=detect_series(rel),
                    )
                )
            except Exception:
                continue
    return docs


def find_reference_targets(source: Doc, by_name: Dict[str, List[str]], by_rel_path: Dict[str, str]) -> Set[str]:
    targets: Set[str] = set()
    source_name = Path(source.path).name
    lower_text = source.text.lower()
    for candidate in REFERENCE_RE.findall(source.text):
        normalized_candidate = candidate.replace("\\", "/").lstrip("./").lower()
        if normalized_candidate in by_rel_path and by_rel_path[normalized_candidate] != source.path:
            targets.add(by_rel_path[normalized_candidate])
            continue
        key = Path(normalized_candidate).name
        for target_path in by_name.get(key, []):
            if target_path != source.path:
                targets.add(target_path)
    for file_name, target_paths in by_name.items():
        if file_name == source_name.lower():
            continue
        if file_name in lower_text:
            for target_path in target_paths:
                if target_path != source.path:
                    targets.add(target_path)
    return targets


def build_graph(
    docs: List[Doc], threshold_percent: float = 4.0
) -> Tuple[Dict, List[Dict], Dict[str, int], Dict[str, List[str]]]:
    nodes = []
    edges = []
    associations: List[Dict] = []
    counts_by_language: Dict[str, int] = {"Python": 0, "HTML": 0, "PHP": 0}
    series_map: Dict[str, List[str]] = {}
    by_path = {d.path: d for d in docs}
    by_name: Dict[str, List[str]] = {}
    by_rel_path = {d.path.lower(): d.path for d in docs}
    for d in docs:
        by_name.setdefault(Path(d.path).name.lower(), []).append(d.path)

    for d in docs:
        counts_by_language[d.language] = counts_by_language.get(d.language, 0) + 1
        series_map.setdefault(d.series, []).append(d.path)
        nodes.append({
            "id": d.path,
            "label": Path(d.path).name,
            "group": d.language,
            "title": f"{d.path}\nLangage: {d.language}\nSérie: {d.series}",
            "value": 20,
        })

    seen_edges: Set[Tuple[str, str, str]] = set()

    for source in docs:
        for target in sorted(find_reference_targets(source, by_name, by_rel_path)):
            key = (source.path, target, "reference")
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(
                {
                    "from": source.path,
                    "to": target,
                    "value": 2.5,
                    "title": "Référence directe",
                    "percent": 100.0,
                    "relation": "reference",
                }
            )
            associations.append(
                {
                    "type": "reference",
                    "from": source.path,
                    "to": target,
                    "from_language": source.language,
                    "to_language": by_path[target].language,
                }
            )

    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            score = cosine_similarity(docs[i].text, docs[j].text)
            pct = round(score * 100, 2)
            if pct >= threshold_percent:
                relation = "cross_language_similarity" if docs[i].language != docs[j].language else "similarity"
                edges.append({
                    "from": docs[i].path,
                    "to": docs[j].path,
                    "value": max(1.0, score * 10.0),
                    "title": f"Similarité: {pct}%",
                    "percent": pct,
                    "relation": relation,
                })
                associations.append(
                    {
                        "type": relation,
                        "from": docs[i].path,
                        "to": docs[j].path,
                        "from_language": docs[i].language,
                        "to_language": docs[j].language,
                        "score_percent": pct,
                    }
                )

    for files in series_map.values():
        files.sort()
    return {"nodes": nodes, "edges": edges}, associations, counts_by_language, series_map


def build_summary(
    docs: List[Doc], associations: List[Dict], counts_by_language: Dict[str, int], series_map: Dict[str, List[str]]
) -> Dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(docs),
        "counts_by_language": counts_by_language,
        "series": [
            {"name": series, "files": files}
            for series, files in sorted(series_map.items())
        ],
        "associations": associations,
    }


def build_markdown(summary: Dict) -> str:
    lines = [
        "# Synthèse de corrélation Python / HTML / PHP",
        "",
        f"- Généré le: `{summary['generated_at']}`",
        f"- Total de fichiers détectés: **{summary['total_files']}**",
        "",
        "## Comptage par langage",
    ]
    for language, count in summary["counts_by_language"].items():
        lines.append(f"- {language}: **{count}**")
    lines.extend(["", "## Séries détectées"])
    for series in summary["series"]:
        lines.append(f"- **{series['name']}** ({len(series['files'])} fichier(s))")
        for file_path in series["files"]:
            lines.append(f"  - `{file_path}`")
    lines.extend(["", "## Associations / couplages"])
    if not summary["associations"]:
        lines.append("- Aucune association détectée avec les seuils courants.")
    else:
        for assoc in summary["associations"]:
            label = assoc["type"]
            score = f" ({assoc['score_percent']}%)" if "score_percent" in assoc else ""
            lines.append(
                f"- `{assoc['from']}` → `{assoc['to']}` : **{label}**{score}"
            )
    return "\n".join(lines) + "\n"


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    docs = load_docs(repo_root)
    if not docs:
        raise SystemExit("Aucun fichier Python/HTML/PHP trouvé dans le repository.")

    graph, associations, counts_by_language, series_map = build_graph(docs, threshold_percent=4.0)
    summary = build_summary(docs, associations, counts_by_language, series_map)
    markdown = build_markdown(summary)

    out = script_dir / "correlation_graph.json"
    summary_out = script_dir / "correlation_summary.json"
    summary_md = script_dir / "correlation_summary.md"
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_md.write_text(markdown, encoding="utf-8")

    print(f"OK -> {out}")
    print(f"OK -> {summary_out}")
    print(f"OK -> {summary_md}")
    print(f"nodes={len(graph['nodes'])}, edges={len(graph['edges'])}")


if __name__ == "__main__":
    main()
