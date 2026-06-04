#!/usr/bin/env python3
"""Generate Ned roadmap views from roadmap/roadmap.yaml.

Canonical source of truth: roadmap/roadmap.yaml
Generated outputs: roadmap.json, roadmap.csv, roadmap.md, index.html
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
from pathlib import Path
from typing import Any

import yaml

STATUS_ORDER = {
    "active": 0,
    "next": 1,
    "planned": 2,
    "conditional": 3,
    "deferred": 4,
    "done": 5,
}

STATUS_LABELS = {
    "done": "Done",
    "active": "Active",
    "next": "Next",
    "planned": "Planned",
    "deferred": "Deferred",
    "conditional": "Conditional",
}

CSV_FIELDS = [
    "id",
    "order",
    "status",
    "track",
    "track_label",
    "phase",
    "title",
    "summary",
    "next_action",
    "dependencies",
    "sources",
    "tags",
    "completed_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_roadmap(source_path: Path) -> dict[str, Any]:
    with source_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Roadmap YAML must be a mapping")
    validate_roadmap(data)
    return data


def validate_roadmap(data: dict[str, Any]) -> None:
    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Roadmap must contain a non-empty items list")

    tracks = data.get("tracks", {})
    ids: set[str] = set()
    orders: list[int] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item {index} must be a mapping")
        for required in ["id", "order", "track", "status", "title", "summary", "next_action"]:
            if required not in item:
                raise ValueError(f"Item {item.get('id', index)} is missing {required}")
        item_id = item["id"]
        if item_id in ids:
            raise ValueError(f"Duplicate item id: {item_id}")
        ids.add(item_id)
        if item["track"] not in tracks:
            raise ValueError(f"Unknown track for {item_id}: {item['track']}")
        if item["status"] not in STATUS_LABELS:
            raise ValueError(f"Unknown status for {item_id}: {item['status']}")
        if not isinstance(item["order"], int):
            raise ValueError(f"Order for {item_id} must be an integer")
        orders.append(item["order"])

    if len(orders) != len(set(orders)):
        raise ValueError("Roadmap order values must be unique")

    known_ids = ids
    for item in items:
        for dependency in item.get("dependencies") or []:
            if dependency not in known_ids:
                raise ValueError(f"Unknown dependency for {item['id']}: {dependency}")


def sorted_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(data["items"], key=lambda item: (item["order"], item["id"]))


def normalize_value(value: Any) -> Any:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_value(item) for key, item in value.items()}
    return value


def enriched_data(data: dict[str, Any]) -> dict[str, Any]:
    copy = normalize_value(dict(data))
    copy["status_labels"] = STATUS_LABELS
    copy["items"] = []
    for item in sorted_items(data):
        enriched = normalize_value(dict(item))
        enriched["track_label"] = data["tracks"][item["track"]]
        enriched["status_label"] = STATUS_LABELS[item["status"]]
        copy["items"].append(enriched)
    return copy


def list_to_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def write_json(data: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(data: dict[str, Any], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for item in data["items"]:
            writer.writerow({field: list_to_cell(item.get(field)) for field in CSV_FIELDS})


def write_markdown(data: dict[str, Any], output_path: Path) -> None:
    lines: list[str] = []
    lines.append(f"# {data['name']}")
    lines.append("")
    lines.append(data.get("description", ""))
    lines.append("")
    lines.append("> Generated from `roadmap/roadmap.yaml`. Reorder work by changing item `order` values, then run `python3 scripts/generate-roadmap.py`.")
    lines.append("")

    counts: dict[str, int] = {status: 0 for status in STATUS_LABELS}
    for item in data["items"]:
        counts[item["status"]] += 1
    lines.append("## Status summary")
    lines.append("")
    for status, label in STATUS_LABELS.items():
        lines.append(f"- **{label}:** {counts[status]}")
    lines.append("")

    for track_id, track_label in data["tracks"].items():
        track_items = [item for item in data["items"] if item["track"] == track_id]
        if not track_items:
            continue
        lines.append(f"## {track_label}")
        lines.append("")
        for item in track_items:
            phase = f"Phase {item['phase']}" if item.get("phase") is not None else "No phase"
            lines.append(f"### {item['order']}. {item['title']} — {item['status_label']} ({phase})")
            lines.append("")
            lines.append(f"{item['summary']}")
            lines.append("")
            lines.append(f"- **Next action:** {item['next_action']}")
            if item.get("dependencies"):
                lines.append(f"- **Depends on:** {', '.join(item['dependencies'])}")
            if item.get("sources"):
                lines.append(f"- **Sources:** {', '.join(item['sources'])}")
            lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def make_html(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    safe_payload = payload.replace("</", "<\\/")
    escaped_yaml_hint = html.escape("Change order values in roadmap.yaml or use dashboard export.")
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Ned End-to-End Roadmap</title>
<style>
:root {{
  --bg: #08111f; --panel: rgba(15, 23, 42, .88); --panel2: rgba(30, 41, 59, .82);
  --text: #e5edf7; --muted: #93a4b8; --line: rgba(148, 163, 184, .24);
  --blue: #60a5fa; --green: #34d399; --amber: #fbbf24; --purple: #a78bfa;
  --red: #fb7185; --cyan: #22d3ee;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top left, #12345a 0, transparent 35rem), radial-gradient(circle at top right, #35245f 0, transparent 32rem), var(--bg); color: var(--text); }}
header {{ padding: 36px clamp(18px, 4vw, 56px) 20px; }}
h1 {{ margin: 0; font-size: clamp(2rem, 5vw, 4.6rem); letter-spacing: -0.07em; line-height: .95; }}
.subtitle {{ max-width: 900px; color: var(--muted); font-size: 1.05rem; line-height: 1.6; margin-top: 16px; }}
.controls {{ display: grid; grid-template-columns: 1fr repeat(3, minmax(150px, 210px)); gap: 12px; padding: 0 clamp(18px, 4vw, 56px) 18px; position: sticky; top: 0; z-index: 5; background: linear-gradient(to bottom, rgba(8,17,31,.96), rgba(8,17,31,.78)); backdrop-filter: blur(18px); }}
input, select, button, textarea {{ border: 1px solid var(--line); background: rgba(15, 23, 42, .92); color: var(--text); border-radius: 14px; padding: 12px 14px; font: inherit; }}
button {{ cursor: pointer; background: linear-gradient(135deg, rgba(96,165,250,.2), rgba(167,139,250,.16)); }}
main {{ padding: 0 clamp(18px, 4vw, 56px) 56px; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 14px 0 24px; }}
.stat {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 16px; }}
.stat b {{ display: block; font-size: 1.8rem; }}
.tabs {{ display:flex; gap: 8px; flex-wrap: wrap; margin: 18px 0; }}
.tab {{ border-radius: 999px; padding: 9px 13px; color: var(--muted); border: 1px solid var(--line); background: rgba(15,23,42,.65); }}
.tab.active {{ color: var(--text); border-color: rgba(96,165,250,.8); }}
.view {{ display: none; }} .view.active {{ display: block; }}
.lanes {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; align-items: start; }}
.lane {{ background: rgba(15,23,42,.58); border: 1px solid var(--line); border-radius: 24px; padding: 14px; min-height: 220px; }}
.lane h2 {{ margin: 4px 4px 14px; font-size: 1rem; color: var(--muted); }}
.card {{ background: linear-gradient(180deg, rgba(30,41,59,.94), rgba(15,23,42,.94)); border: 1px solid var(--line); border-left: 4px solid var(--blue); border-radius: 20px; padding: 14px; margin: 10px 0; box-shadow: 0 20px 48px rgba(0,0,0,.22); }}
.card.done {{ border-left-color: var(--green); opacity: .78; }} .card.active {{ border-left-color: var(--cyan); }} .card.next {{ border-left-color: var(--amber); }} .card.planned {{ border-left-color: var(--purple); }} .card.deferred {{ border-left-color: var(--red); }} .card.conditional {{ border-left-color: #f97316; }}
.card h3 {{ margin: 8px 0 6px; font-size: 1.05rem; }} .card p {{ color: var(--muted); line-height: 1.45; margin: 6px 0; }}
.meta {{ display:flex; gap: 7px; flex-wrap: wrap; }}
.chip {{ font-size: .78rem; padding: 4px 8px; border-radius: 999px; background: rgba(148,163,184,.14); color: #cbd5e1; }}
.order {{ color: var(--blue); font-weight: 800; }}
details {{ margin-top: 10px; color: var(--muted); }} summary {{ cursor: pointer; color: var(--text); }}
.timeline {{ position: relative; margin-left: 10px; padding-left: 26px; border-left: 1px solid var(--line); }}
.timeline .card {{ position: relative; }} .timeline .card:before {{ content: attr(data-order); position: absolute; left: -48px; top: 18px; width: 34px; height: 34px; border-radius: 999px; display:grid; place-items:center; background: #0f172a; border: 1px solid var(--line); color: var(--blue); font-size: .75rem; font-weight: 800; }}
table {{ width: 100%; border-collapse: collapse; background: var(--panel); border-radius: 18px; overflow: hidden; }}
th, td {{ padding: 11px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }} th {{ color: var(--muted); font-weight: 600; }}
.editor {{ display:grid; grid-template-columns: minmax(280px, 460px) 1fr; gap: 16px; }}
textarea {{ width: 100%; min-height: 540px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: .88rem; line-height: 1.4; }}
.help {{ color: var(--muted); line-height: 1.55; background: var(--panel); border:1px solid var(--line); border-radius: 18px; padding: 16px; }}
@media (max-width: 900px) {{ .controls {{ grid-template-columns: 1fr; position: static; }} .editor {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <h1>Ned End-to-End Roadmap</h1>
  <div class=\"subtitle\">Everything known on the Ned roadmap — completed, active, planned, deferred, and conditional. Source of truth is <code>roadmap/roadmap.yaml</code>. {escaped_yaml_hint}</div>
</header>
<section class=\"controls\">
  <input id=\"search\" placeholder=\"Search title, summary, tags, sources…\" />
  <select id=\"statusFilter\"><option value=\"all\">All statuses</option></select>
  <select id=\"trackFilter\"><option value=\"all\">All tracks</option></select>
  <button id=\"copyJson\">Copy JSON</button>
</section>
<main>
  <section class=\"stats\" id=\"stats\"></section>
  <nav class=\"tabs\">
    <button class=\"tab active\" data-view=\"timeline\">Timeline</button>
    <button class=\"tab\" data-view=\"lanes\">Track lanes</button>
    <button class=\"tab\" data-view=\"table\">Table</button>
    <button class=\"tab\" data-view=\"editor\">Reorder/export</button>
  </nav>
  <section id=\"timeline\" class=\"view active\"><div class=\"timeline\" id=\"timelineList\"></div></section>
  <section id=\"lanes\" class=\"view\"><div class=\"lanes\" id=\"laneList\"></div></section>
  <section id=\"table\" class=\"view\"><div id=\"tableList\"></div></section>
  <section id=\"editor\" class=\"view\">
    <div class=\"editor\">
      <div class=\"help\">
        <h2>How to change order of operations</h2>
        <p>Use the table below as an editing aid. Change the numbers, click <b>Rebuild YAML snippet</b>, then copy the generated YAML block back into <code>roadmap/roadmap.yaml</code> or send it to Ned/Hermes.</p>
        <p>The stable <code>id</code> is the anchor. The <code>order</code> number controls sequence. Leave gaps like 10, 20, 30 so inserting work is easy.</p>
        <button id=\"renumber\">Renumber visible by 10s</button>
        <button id=\"buildYaml\">Rebuild YAML snippet</button>
        <button id=\"copyYaml\">Copy edited YAML</button>
      </div>
      <div><textarea id=\"yamlOut\"></textarea></div>
    </div>
  </section>
</main>
<script>
const ROADMAP_DATA = {safe_payload};
let items = ROADMAP_DATA.items.map(x => ({{...x}}));
const statusLabels = ROADMAP_DATA.status_labels;
const statusOrder = {{active:0,next:1,planned:2,conditional:3,deferred:4,done:5}};
const search = document.querySelector('#search');
const statusFilter = document.querySelector('#statusFilter');
const trackFilter = document.querySelector('#trackFilter');

function escapeHtml(value) {{ return String(value ?? '').replace(/[&<>\"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}}[c])); }}
function itemText(item) {{ return [item.id,item.title,item.summary,item.next_action,item.track_label,item.status_label,(item.tags||[]).join(' '),(item.sources||[]).join(' ')].join(' ').toLowerCase(); }}
function filteredItems() {{
  const q = search.value.trim().toLowerCase();
  return items.filter(item => (statusFilter.value === 'all' || item.status === statusFilter.value) && (trackFilter.value === 'all' || item.track === trackFilter.value) && (!q || itemText(item).includes(q))).sort((a,b) => a.order - b.order || a.id.localeCompare(b.id));
}}
function card(item, editable=false) {{
  const deps = (item.dependencies||[]).length ? `<p><b>Depends:</b> ${{escapeHtml(item.dependencies.join(', '))}}</p>` : '';
  const sources = (item.sources||[]).length ? `<p><b>Sources:</b> ${{escapeHtml(item.sources.join(', '))}}</p>` : '';
  const tags = (item.tags||[]).map(t => `<span class=\"chip\">#${{escapeHtml(t)}}</span>`).join('');
  const orderControl = editable ? `<input data-id=\"${{escapeHtml(item.id)}}\" class=\"orderInput\" type=\"number\" value=\"${{item.order}}\" />` : `<span class=\"order\">${{item.order}}</span>`;
  return `<article class=\"card ${{item.status}}\" data-order=\"${{item.order}}\"><div class=\"meta\">${{orderControl}}<span class=\"chip\">${{escapeHtml(item.status_label)}}</span><span class=\"chip\">${{escapeHtml(item.track_label)}}</span><span class=\"chip\">Phase ${{escapeHtml(item.phase)}}</span>${{tags}}</div><h3>${{escapeHtml(item.title)}}</h3><p>${{escapeHtml(item.summary)}}</p><details><summary>Details</summary><p><b>Next:</b> ${{escapeHtml(item.next_action)}}</p>${{deps}}${{sources}}</details></article>`;
}}
function renderStats(list) {{
  const total = list.length;
  const byStatus = Object.fromEntries(Object.keys(statusLabels).map(s => [s,0]));
  list.forEach(item => byStatus[item.status]++);
  document.querySelector('#stats').innerHTML = [`<div class=\"stat\"><b>${{total}}</b><span>Total visible</span></div>`, ...Object.entries(byStatus).map(([s,n]) => `<div class=\"stat\"><b>${{n}}</b><span>${{escapeHtml(statusLabels[s])}}</span></div>`)].join('');
}}
function renderTimeline(list) {{ document.querySelector('#timelineList').innerHTML = list.map(item => card(item)).join(''); }}
function renderLanes(list) {{
  document.querySelector('#laneList').innerHTML = Object.entries(ROADMAP_DATA.tracks).map(([track,label]) => {{
    const laneItems = list.filter(item => item.track === track);
    return `<section class=\"lane\"><h2>${{escapeHtml(label)}} (${{laneItems.length}})</h2>${{laneItems.map(item => card(item)).join('') || '<p class=\"subtitle\">No matching items.</p>'}}</section>`;
  }}).join('');
}}
function renderTable(list) {{
  document.querySelector('#tableList').innerHTML = `<table><thead><tr><th>Order</th><th>Status</th><th>Track</th><th>Title</th><th>Next action</th></tr></thead><tbody>${{list.map(item => `<tr><td>${{item.order}}</td><td>${{escapeHtml(item.status_label)}}</td><td>${{escapeHtml(item.track_label)}}</td><td><b>${{escapeHtml(item.title)}}</b><br><span style=\"color:var(--muted)\">${{escapeHtml(item.summary)}}</span></td><td>${{escapeHtml(item.next_action)}}</td></tr>`).join('')}}</tbody></table>`;
}}
function renderEditor(list) {{
  document.querySelector('#yamlOut').value = buildYamlSnippet(list);
}}
function buildYamlSnippet(list) {{
  return list.map(item => `- id: ${{item.id}}\n  order: ${{item.order}}\n  status: ${{item.status}}\n  title: ${{item.title}}`).join('\\n\\n');
}}
function render() {{ const list = filteredItems(); renderStats(list); renderTimeline(list); renderLanes(list); renderTable(list); renderEditor(list); }}
function initFilters() {{
  Object.entries(statusLabels).forEach(([value,label]) => statusFilter.insertAdjacentHTML('beforeend', `<option value=\"${{value}}\">${{escapeHtml(label)}}</option>`));
  Object.entries(ROADMAP_DATA.tracks).forEach(([value,label]) => trackFilter.insertAdjacentHTML('beforeend', `<option value=\"${{value}}\">${{escapeHtml(label)}}</option>`));
}}
document.querySelectorAll('.tab').forEach(btn => btn.addEventListener('click', () => {{ document.querySelectorAll('.tab,.view').forEach(el => el.classList.remove('active')); btn.classList.add('active'); document.querySelector('#' + btn.dataset.view).classList.add('active'); }}));
[search,statusFilter,trackFilter].forEach(el => el.addEventListener('input', render));
document.querySelector('#copyJson').addEventListener('click', () => navigator.clipboard.writeText(JSON.stringify(ROADMAP_DATA, null, 2)));
document.querySelector('#renumber').addEventListener('click', () => {{ filteredItems().forEach((item, idx) => {{ const real = items.find(x => x.id === item.id); real.order = (idx + 1) * 10; }}); render(); }});
document.querySelector('#buildYaml').addEventListener('click', render);
document.querySelector('#copyYaml').addEventListener('click', () => navigator.clipboard.writeText(document.querySelector('#yamlOut').value));
document.addEventListener('input', e => {{ if (e.target.classList && e.target.classList.contains('orderInput')) {{ const real = items.find(x => x.id === e.target.dataset.id); real.order = Number(e.target.value); renderEditor(filteredItems()); }} }});
initFilters(); render();
</script>
</body>
</html>
"""


def write_html(data: dict[str, Any], output_path: Path) -> None:
    output_path.write_text(make_html(data), encoding="utf-8")


def generate(source_path: Path, output_dir: Path) -> list[Path]:
    data = enriched_data(load_roadmap(source_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        output_dir / "roadmap.json",
        output_dir / "roadmap.csv",
        output_dir / "roadmap.md",
        output_dir / "index.html",
    ]
    write_json(data, outputs[0])
    write_csv(data, outputs[1])
    write_markdown(data, outputs[2])
    write_html(data, outputs[3])
    return outputs


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=root / "roadmap" / "roadmap.yaml")
    parser.add_argument("--out", type=Path, default=root / "roadmap")
    args = parser.parse_args()
    outputs = generate(args.source, args.out)
    print("Generated roadmap outputs:")
    for output in outputs:
        print(f"- {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
