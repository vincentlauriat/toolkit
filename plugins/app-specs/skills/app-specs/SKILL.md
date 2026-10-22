---
name: app-specs
description: Use when the user wants to frame, specify or kick off an app or product — a new idea, an existing codebase to document, or existing specs to update. Asks for a PRD, TRD, app flow, UI/UX design brief, backend schema or implementation plan, says "cadrer une app", "cahier des charges", "specs", "mettre à jour les specs", "/app-specs", or starts an empty project with only an idea.
---

# App specs — interview then 6 framing documents

## Overview

Turn an app idea into six consistent framing documents by **interviewing the user first**, in short rounds, then writing everything at once. Never leave a placeholder: every field is either answered by the user, or filled with an explicit, flagged assumption.

| # | File | Purpose |
|---|---|---|
| 1 | `PRD.md` | What the product does, how success is measured, what could go wrong |
| 2 | `TRD.md` | Explicit technical choices, tests, run cost |
| 3 | `AppFlow.md` | Every screen, path and state |
| 4 | `DesignBrief.md` | Visual direction and UX rules |
| 5 | `BackendSchema.md` | Data, relations, access rules |
| 6 | `ImplementationPlan.md` | Build order, effort, checkpoints, traceability table |

Section structure for each file: `templates.md` in this directory. Read it before writing. In it, `{{...}}` marks a placeholder to replace — never copy `{{` into a document. Checker: `check.py` in this directory.

**Language.** Everything the skill says or asks is in the user's language. The option labels below are written in French: translate them when the user speaks another language.

**Output folder: `docs/specs/`** (create it). Exception: if the 6 files already exist at the project root, keep them there.

## Step 0 — Pick the mode

Look at the working directory and the invocation args before asking anything.

| Situation | Mode |
|---|---|
| The 6 files exist (`docs/specs/` or root) | **Update** |
| Source code exists (`package.json`, `Package.swift`, `*.xcodeproj`, `pyproject.toml`, `src/`…) and no specs | Ask once via `AskUserQuestion`: *Documenter l'existant* / *Cadrer une évolution ou une refonte* / *Repartir de zéro*. First choice → **Existing project** |
| Empty folder, or "repartir de zéro" | **New app** (the default flow below) |

## Interview (New app)

Ask in the user's language. Use `AskUserQuestion` for choices (max 4 questions per call, recommended option first with "(Recommandé)"), plain chat for open answers.

- **Skip what is already known.** Before each round, drop questions answered by the invocation args, earlier free-text answers (e.g. "pour moi et ma famille" answers Audience), or existing project files.
- **"Je ne sais pas / propose"** is always acceptable: pick the option yourself, no follow-up question, and flag it as an assumption.

**Round 1 — the idea (plain chat, one message).** Product name (even provisional), the problem in one sentence, who the users are, what they do today instead. Add one optional line, clearly skippable: reference products to imitate or avoid, brand colors/logo, constraints (deadline, budget, compliance, region).

**Round 2 — framing (`AskUserQuestion`).**
- Platform: Web / macOS natif / Mobile iOS+Android / Autre
- Audience: Moi seul / Équipe interne / Clients B2B / Grand public
- Accounts: Aucun compte / Email (magic link ou mot de passe) / SSO Google-Microsoft / Comptes avec rôles
- Documents language — only if no project convention exists (e.g. a CLAUDE.md rule "doc files in English"). If one exists, don't ask: apply it and state it in the confirmation. An explicit user choice always overrides the convention.

**Round 3 — value and scope (plain chat).** The goal and one measurable success signal; the 3–7 main features (one line each, most important first); what is explicitly out of scope for v1; the main risks the user already sees.

**Round 4 — technique and look (`AskUserQuestion`).** Tailor options to the platform.
- Stack: 2–3 stacks fitting the platform (recommended first)
- Data: Local uniquement / Cloud managé (ex. Supabase, Firebase) / Auto-hébergé / Base existante
- External services (multiSelect): LLM/IA, paiement, email/notifications, cartes/géoloc
- Design tone: 3 contrasting adjective triads (e.g. "sobre, dense, pro" / "chaleureux, ludique, rond" / "premium, aéré, éditorial")

## Existing project mode

Document what is there instead of imagining it.

1. **Read the code first.** For anything beyond a small repo, delegate to an exploration subagent: stack and versions, entry points, screens/routes, data model, external services, auth, tests, CI, release process. Also read the README and any existing docs.
2. **Derive rounds 1–4 from the code**, then ask only what the code cannot tell: the real goal and success metric, the audience, what is intentionally out of scope, planned features. Facts from the code are written `*(constaté : path/to/file)*`; anything inferred is `*(hypothèse)*`.
3. **Priorities.** Shipped features are listed with status « livrée » and get P0 or P1 in the PRD table; planned features follow the normal P0–P2 rules.
4. **ImplementationPlan becomes an evolution plan.** Steps cover only the gap between code and PRD (missing features, quality, release). Traceability rows for shipped features put `existant : path` in Tasks (non-empty, as the checker requires).
5. Then continue at *Confirmation* below. Contradictions between the code and the user's intent are the most valuable thing to surface there.

## Update mode

Specs exist; do not re-run the interview.

1. Read all six files. Ask once via `AskUserQuestion` (multiSelect): *Ajouter/modifier une fonctionnalité* / *Changement technique* / *Resynchroniser avec le code* / *Autre*, then one plain-chat question on the details.
2. Run the *Confirmation* step on the **delta only**: what changes, what ripples into other documents, new contradictions.
3. Edit **in place**, never regenerate a file: the user may have hand-edited it. Propagate in dependency order (PRD → … → ImplementationPlan) and keep names verbatim. A removed feature loses its traceability row; an added one gets one.
4. Append a line to the PRD's **Revision log** (date, change, documents touched).
5. Run the checker, then report what changed per file.

## Confirmation (before writing anything)

Present, in ≤25 lines:
1. **Summary** — name, problem, users, platform, stack, docs language, output folder.
2. **Features with priorities** — P0 = v1 must-have, P1 = v1 if time, P2 = later. If the user gave none, derive them from order and wording. Mark features you added yourself as « proposée » so the user sees them before accepting.
3. **Contradictions found, each with your proposed resolution** — e.g. "local-only data + external LLM → API key needs a small server proxy". Also check that the success metric can actually be measured by some feature; if not, propose the missing feature.
4. **Main assumptions** you will make.

Then ask "Je génère ?" via `AskUserQuestion` (Générer / Corriger quelque chose).

## Writing

1. Write in dependency order: PRD → TRD → AppFlow → DesignBrief → BackendSchema → ImplementationPlan. Reuse PRD feature names, entity names and screen names verbatim in every later doc.
2. Flag your own choices with `*(hypothèse)*` (`*(assumption)*` in English docs): per value when the user answered the rest of the section; once at the section heading when the whole section is yours (e.g. a DesignBrief when the user gave no reference or brand).
3. PRD **Open questions**: numbered, each with your recommendation; include every assumption that changes scope, cost, architecture or data handling, plus the resolved contradictions. Cosmetic values (hex codes, px sizes) stay flagged in place only.
4. Scale to the audience: a solo/local tool gets no roles, no staging, no multi-region, a one-line cost estimate. When a template section doesn't apply (e.g. authorization without accounts), write one line saying why instead of a mechanical table.
5. Estimates (run cost, build effort) are orders of magnitude with their basis, never false precision; flag them as hypotheses.
6. Follow the project's own conventions if it has any (tracking files like CHANGES.md/TODOS.md, .gitignore rules).

## Verification (before announcing done)

Run the shipped checker — do not rewrite it, do not use grep:

```bash
python3 -I <skill-dir>/check.py <output-folder> --self-test
python3 -I <skill-dir>/check.py <output-folder>
```

`<skill-dir>` is the directory holding this file. The checker verifies:
- the 6 files exist and are non-empty;
- no `{{` remains;
- the **Traceability** table has one row per P0/P1 feature of the PRD, with non-empty Screens and Tasks cells, and every screen/entity named there exists in AppFlow / BackendSchema (exact whole-item match);
- every entity (`- **Name** —` lines of BackendSchema's Entities section) is named in the authorization section;
- Mermaid blocks start with a known diagram type and have balanced brackets. This is a static check only: if `mmdc` is installed, also render each block.

`--self-test` first needs a passing baseline (if the documents fail, fix them and rerun). It then mutates copies of the real documents (placeholder inserted, empty file, traceability row removed) and all three mutations must be caught.

Fix gaps, then give the user: the file list, the top 3–5 open questions, and the suggested next step (step 1 of the implementation plan). Quote the checker's last line rather than just saying it passed.

## Common mistakes

| Mistake | Fix |
|---|---|
| Asking all ~40 template fields one by one | 4 short rounds; derive the rest and flag as assumptions |
| Re-asking what free text already answered | Skip it; restate it in the confirmation instead |
| Resolving contradictory answers silently | Surface them in the confirmation with a proposed resolution |
| Success metric that no feature can measure | Propose the missing feature in the confirmation |
| Generic filler ("modern, clean UI", "fast") | Concrete values: hex colors, px sizes, ms targets, named screens |
| Feature names drifting between documents | Reuse PRD names verbatim; the traceability table exposes drift |
| Over-engineering a solo/local tool | Scale TRD and schema to the audience from round 2 |
| Inventing a stack the code contradicts | Existing project mode: read the code first, cite files |
| Regenerating specs the user hand-edited | Update mode: edit in place, log the change |
