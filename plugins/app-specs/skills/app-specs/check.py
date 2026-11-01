#!/usr/bin/env python3
"""Verify the seven app-specs documents (overview + six).

Usage:
    python3 -I check.py <specs-dir>              check the documents
    python3 -I check.py <specs-dir> --self-test  prove the checker catches failures

Exit code 0 = all checks pass, 1 = at least one failure. Feature and traceability
tables are recognised by their content (P0/P1/P2 cells), not by their headings; the
screen list is the table of 03-user-flows.md whose first header cell is "Screen"
(or its translation, see SCREEN_HEADER).
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

FILES = ["00-overview.md", "01-prd.md", "02-trd.md", "03-user-flows.md", "04-design-brief.md",
         "05-data-model.md", "06-implementation-plan.md"]
PRIO = re.compile(r"^P[0-2]$")
AUTH_HEADING = re.compile(r"authori[sz]ation|autorisation|permission|droits d", re.I)
MERMAID_START = re.compile(
    r"^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(-v2)?|erDiagram|"
    r"journey|gantt|pie|mindmap|timeline|C4Context|quadrantChart|gitGraph)\b")
# Closed list: the first header cell of the UserFlows screen table, optionally followed
# by "list"/"liste" or a parenthesis, e.g. "Screen", "Screens (UserFlows)", "Écran".
SCREEN_HEADER = re.compile(
    r"^(screens?|écrans?|pantallas?|telas?|schermat[ae]|schermi|bildschirme?|ansichte?n?|surfaces?)"
    r"(\s+(list|liste|lista))?(\s*\(.*\))?$", re.I)


def plain(cell):
    """Strip markdown emphasis and code ticks so '**Name**' matches 'Name'.

    Underscores are removed only when they wrap a word ('_Name_'), never inside
    one, so snake_case names such as 'plant_day' survive.
    """
    cell = cell.replace("\\_", "_")
    cell = re.sub(r"[*`]+", "", cell)
    cell = re.sub(r"(?<!\w)(_+)(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", cell)
    return cell.strip()


def tables(text):
    """Yield each markdown table as a list of rows (list of stripped cells), separator row removed."""
    block = []
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            block.append(line.strip())
        elif block:
            rows = [[plain(c) for c in r.strip("|").split("|")] for r in block]
            yield [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
            block = []


def sections(text):
    """Return [(heading, body)] split on markdown headings."""
    parts = re.split(r"^(#{1,6} .*)$", text, flags=re.M)
    return [(parts[i].lstrip("# ").strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def items(cell):
    return [i.strip() for i in cell.split(",") if i.strip()]


def check(d):
    errors = []
    docs = {}
    for name in FILES:
        p = d / name
        if not p.is_file() or not p.read_text(encoding="utf-8").strip():
            errors.append(f"{name}: missing or empty")
        else:
            docs[name] = p.read_text(encoding="utf-8")
    if errors:
        return errors

    for name, text in docs.items():
        if "{{" in text:
            errors.append(f"{name}: unresolved placeholder '{{{{'")
        errors += mermaid_errors(name, text)

    for other in FILES[1:]:
        if other not in docs["00-overview.md"]:
            errors.append(f"00-overview.md: does not link {other}")

    must = prd_must(docs["01-prd.md"])
    if not must:
        errors.append("01-prd.md: no P0/P1 feature row found")

    # Screens from UserFlows: first-column cells of the table(s) headed "Screen".
    screens = {r[0] for t in tables(docs["03-user-flows.md"])
               if t and SCREEN_HEADER.match(t[0][0]) for r in t[1:] if r}
    if not screens:
        errors.append("03-user-flows.md: no screen table found (first header cell 'Screen')")

    # Entities: the first section of DataModel holding '- **Name** —' lines.
    entities = []
    for _, body in sections(docs["05-data-model.md"]):
        found = re.findall(r"^- \*\*(.+?)\*\*\s+—", body, flags=re.M)
        if found:
            entities = [plain(e) for e in found]
            break
    if not entities:
        errors.append("05-data-model.md: no '- **Entity** — ...' line found")

    trace = traceability(docs["06-implementation-plan.md"])
    for f in sorted(must):
        row = trace.get(f)
        if row is None:
            errors.append(f"06-implementation-plan.md: traceability row missing for feature '{f}'")
            continue
        if row[1] != prd_features(docs["01-prd.md"])[f]:
            errors.append(f"06-implementation-plan.md: priority {row[1]} for '{f}' differs from the PRD")
        if not row[2] or not row[-1]:
            errors.append(f"06-implementation-plan.md: empty Screens or Tasks cell for '{f}'")
        for s in items(row[2]):
            if s not in screens:
                errors.append(f"06-implementation-plan.md: screen '{s}' (feature '{f}') not found in the "
                              "03-user-flows.md screen table(s) (first header cell 'Screen')")
        for e in items(row[3]):
            if e not in ("—", "-") and e not in entities:
                errors.append(f"06-implementation-plan.md: entity '{e}' (feature '{f}') not found in 05-data-model.md")
    rows = [r[0] for t in tables(docs["06-implementation-plan.md"]) for r in t
            if len(r) >= 5 and PRIO.match(r[1])]
    for f in sorted({f for f in rows if rows.count(f) > 1}):
        errors.append(f"06-implementation-plan.md: duplicate traceability row for '{f}'")

    # Authorization section names every entity.
    auth = [b for h, b in sections(docs["05-data-model.md"]) if AUTH_HEADING.search(h)]
    if not auth:
        errors.append("05-data-model.md: no authorization section found")
    else:
        for e in entities:
            if not re.search(rf"(?<![\w-]){re.escape(e)}(?![\w-])", auth[0].replace("\\_", "_")):
                errors.append(f"05-data-model.md: entity '{e}' not named in the authorization section")
    return errors


def prd_features(prd):
    """{feature: priority} of the PRD: any table row whose last cell is a priority."""
    return {r[0]: r[-1] for t in tables(prd) for r in t if len(r) >= 3 and PRIO.match(r[-1])}


def prd_must(prd):
    """P0/P1 feature names of the PRD."""
    return {f for f, p in prd_features(prd).items() if p in ("P0", "P1")}


def traceability(plan):
    """Traceability rows of ImplementationPlan: >= 5 cells, 2nd cell P0/P1/P2."""
    return {r[0]: r for t in tables(plan) for r in t if len(r) >= 5 and PRIO.match(r[1])}


def trace_line(plan, feature):
    """Raw markdown line of the traceability row for `feature`."""
    for line in plan.splitlines():
        cells = [plain(c) for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 5 and cells[0] == feature and PRIO.match(cells[1]):
            return line
    raise ValueError(feature)


def mermaid_errors(name, text):
    errs = []
    for m in re.finditer(r"```mermaid\n(.*?)```", text, flags=re.S):
        body = m.group(1).strip()
        if not MERMAID_START.match(body):
            errs.append(f"{name}: mermaid block does not start with a known diagram type")
        if body.startswith("erDiagram"):
            continue  # cardinality operators (||--o{) are legitimately unbalanced
        body = re.sub(r'"[^"]*"', "", body)  # ignore quoted labels
        for a, b in ("()", "[]", "{}"):
            if body.count(a) != body.count(b):
                errs.append(f"{name}: mermaid block has unbalanced '{a}{b}'")
    if text.count("```") % 2:
        errs.append(f"{name}: odd number of ``` fences")
    return errs


def self_test(d):
    """Mutate copies of the real documents; every mutation must make check() fail."""
    for raw, want in (("**Name**", "Name"), ("`plant_day`", "plant_day"), ("_Name_", "Name"),
                      ("**`plant_day`**", "plant_day"), ("plant\\_day", "plant_day"), ("_meta", "_meta"),
                      ("`_id`", "_id")):
        if plain(raw) != want:
            print(f"FAIL plain({raw!r}) = {plain(raw)!r}, expected {want!r}")
            return 1
    errs = check(d)
    if errs:
        for e in errs:
            print("FAIL", e)
        print("self-test needs a passing baseline; fix the documents first")
        return 1
    plan = (d / "06-implementation-plan.md").read_text(encoding="utf-8")
    must = prd_must((d / "01-prd.md").read_text(encoding="utf-8"))
    feature = next((f for f in sorted(must) if f in traceability(plan)), None)
    if feature is None:
        print("self-test needs a traceability row for a P0/P1 feature of the PRD")
        return 1
    row = trace_line(plan, feature)
    cells = row.split("|")
    cells[3] = " Nonexistent screen "  # cells[0] is the empty text before the first '|'
    bad_screen = "|".join(cells)
    mutations = {
        "placeholder inserted": ("02-trd.md", lambda t: t + "\n{{test}}\n"),
        "empty file": ("04-design-brief.md", lambda t: ""),
        "overview link removed": ("00-overview.md", lambda t: t.replace("06-implementation-plan.md", "")),
        "traceability row removed": ("06-implementation-plan.md", lambda t: t.replace(row + "\n", "", 1)),
        "unknown screen in traceability": ("06-implementation-plan.md", lambda t: t.replace(row, bad_screen, 1)),
    }
    bad = 0
    for label, (fname, fn) in mutations.items():
        with tempfile.TemporaryDirectory() as tmp:
            cp = Path(tmp)
            for f in FILES:
                shutil.copy(d / f, cp / f)
            (cp / fname).write_text(fn((cp / fname).read_text(encoding="utf-8")), encoding="utf-8")
            caught = bool(check(cp))
        print(f"{'OK  ' if caught else 'FAIL'} checker catches: {label}")
        bad += not caught
    n = len(mutations)
    print(f"OK: self-test passed ({n}/{n} mutations caught)" if not bad
          else f"self-test FAILED ({bad}/{n} mutations not caught)")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    root = Path(args[0])
    if "--self-test" in sys.argv:
        sys.exit(self_test(root))
    errs = check(root)
    for e in errs:
        print("FAIL", e)
    print("OK: all checks pass" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
