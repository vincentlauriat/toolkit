#!/usr/bin/env python3
"""Verify the six app-specs documents.

Usage:
    python3 -I check.py <specs-dir>              check the documents
    python3 -I check.py <specs-dir> --self-test  prove the checker catches failures

Exit code 0 = all checks pass, 1 = at least one failure. Language-agnostic:
tables are recognised by their content (P0/P1/P2 cells), not by their headings.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

FILES = ["PRD.md", "TRD.md", "AppFlow.md", "DesignBrief.md",
         "BackendSchema.md", "ImplementationPlan.md"]
PRIO = re.compile(r"^P[0-2]$")
AUTH_HEADING = re.compile(r"authori[sz]ation|autorisation|permission|droits d", re.I)
MERMAID_START = re.compile(
    r"^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(-v2)?|erDiagram|"
    r"journey|gantt|pie|mindmap|timeline|C4Context|quadrantChart|gitGraph)\b")


def plain(cell):
    """Strip markdown emphasis and code ticks so '**Name**' matches 'Name'."""
    return re.sub(r"[*_`]+", "", cell).strip()


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

    # Features (P0/P1) from the PRD: any table row whose last cell is a priority.
    features = {}
    for t in tables(docs["PRD.md"]):
        for r in t:
            if len(r) >= 3 and PRIO.match(r[-1]):
                features[r[0]] = r[-1]
    must = {f for f, p in features.items() if p in ("P0", "P1")}
    if not must:
        errors.append("PRD.md: no P0/P1 feature row found")

    # Screens from AppFlow: first-column cells of every table, plus headings.
    screens = {r[0] for t in tables(docs["AppFlow.md"]) for r in t if r}
    screens |= {h for h, _ in sections(docs["AppFlow.md"])}

    # Entities: the first section of BackendSchema holding '- **Name** —' lines.
    entities = []
    for _, body in sections(docs["BackendSchema.md"]):
        found = re.findall(r"^- \*\*(.+?)\*\*\s+—", body, flags=re.M)
        if found:
            entities = found
            break
    if not entities:
        errors.append("BackendSchema.md: no '- **Entity** — ...' line found")

    # Traceability: rows whose 2nd cell is P0/P1 in ImplementationPlan.
    trace = {}
    for t in tables(docs["ImplementationPlan.md"]):
        for r in t:
            if len(r) >= 5 and PRIO.match(r[1]):
                trace[r[0]] = r
    for f in sorted(must):
        row = trace.get(f)
        if row is None:
            errors.append(f"ImplementationPlan.md: traceability row missing for feature '{f}'")
            continue
        if not row[2] or not row[-1]:
            errors.append(f"ImplementationPlan.md: empty Screens or Tasks cell for '{f}'")
        for s in items(row[2]):
            if s not in screens:
                errors.append(f"ImplementationPlan.md: screen '{s}' (feature '{f}') not found in AppFlow.md")
        for e in items(row[3]):
            if e not in ("—", "-") and e not in entities:
                errors.append(f"ImplementationPlan.md: entity '{e}' (feature '{f}') not found in BackendSchema.md")

    # Authorization section names every entity.
    auth = [b for h, b in sections(docs["BackendSchema.md"]) if AUTH_HEADING.search(h)]
    if not auth:
        errors.append("BackendSchema.md: no authorization section found")
    else:
        for e in entities:
            if not re.search(rf"(?<![\w-]){re.escape(e)}(?![\w-])", auth[0]):
                errors.append(f"BackendSchema.md: entity '{e}' not named in the authorization section")
    return errors


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
    if check(d):
        print("self-test needs a passing baseline; fix the documents first")
        return 1
    plan = (d / "ImplementationPlan.md").read_text(encoding="utf-8")
    trace_rows = [l for l in plan.splitlines()
                  if l.startswith("|") and re.search(r"\|\s*P[01]\s*\|", l)]
    mutations = {
        "placeholder inserted": ("TRD.md", lambda t: t + "\n{{test}}\n"),
        "empty file": ("DesignBrief.md", lambda t: ""),
        "traceability row removed": ("ImplementationPlan.md", lambda t: t.replace(trace_rows[0] + "\n", "", 1)),
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
