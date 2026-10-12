---
name: app-specs
description: Use when the user wants to frame, specify or kick off a new app or product before coding — asks for a PRD, TRD, app flow, UI/UX design brief, backend schema or implementation plan, says "cadrer une app", "cahier des charges", "specs", "/app-specs", or starts an empty project with only an idea.
---

# App specs — interview then 6 framing documents

## Overview

Turn an app idea into six consistent framing documents by **interviewing the user first**, in short rounds, then writing everything at once. Never leave a placeholder: every field is either answered by the user, or filled with an explicit, flagged assumption.

| # | File | Purpose |
|---|---|---|
| 1 | `PRD.md` | What the product does and how success is measured |
| 2 | `TRD.md` | Explicit technical choices |
| 3 | `AppFlow.md` | Every screen, path and state |
| 4 | `DesignBrief.md` | Visual direction and UX rules |
| 5 | `BackendSchema.md` | Data, relations, access rules |
| 6 | `ImplementationPlan.md` | Build order, checkpoints, traceability table |

Section structure for each file: `templates.md` in this directory. Read it before writing. In it, `{{...}}` marks a placeholder to replace — never copy `{{` into a document.

## Interview

Ask in the user's language. Use `AskUserQuestion` for choices (max 4 questions per call, recommended option first with "(Recommandé)"), plain chat for open answers.

- **Skip what is already known.** Before each round, drop questions answered by the invocation args, earlier free-text answers (e.g. "pour moi et ma famille" answers Audience), or existing project files.
- **"Je ne sais pas / propose"** is always acceptable: pick the option yourself, no follow-up question, and flag it as an assumption.

**Round 1 — the idea (plain chat, one message).** Product name (even provisional), the problem in one sentence, who the users are, what they do today instead.

**Round 2 — framing (`AskUserQuestion`).**
- Platform: Web / macOS natif / Mobile iOS+Android / Autre
- Audience: Moi seul / Équipe interne / Clients B2B / Grand public
- Accounts: Aucun compte / Email (magic link ou mot de passe) / SSO Google-Microsoft / Comptes avec rôles
- Documents language — only if no project convention exists (e.g. a CLAUDE.md rule "doc files in English"). If one exists, don't ask: apply it and state it in the confirmation. An explicit user choice always overrides the convention.

**Round 3 — value and scope (plain chat).** The goal and one measurable success signal; the 3–7 main features (one line each, most important first); what is explicitly out of scope for v1.

**Round 4 — technique and look (`AskUserQuestion`).** Tailor options to the platform.
- Stack: 2–3 stacks fitting the platform (recommended first)
- Data: Local uniquement / Cloud managé (ex. Supabase, Firebase) / Auto-hébergé / Base existante
- External services (multiSelect): LLM/IA, paiement, email/notifications, cartes/géoloc
- Design tone: 3 contrasting adjective triads (e.g. "sobre, dense, pro" / "chaleureux, ludique, rond" / "premium, aéré, éditorial")

**Round 5 — optional details (plain chat, one message).** Reference products to imitate or avoid, brand colors/logo, constraints (deadline, budget, compliance, region). Say it can be skipped.

## Confirmation (before writing anything)

Present, in ≤25 lines:
1. **Summary** — name, problem, users, platform, stack, docs language, output folder (project root by default; `docs/specs/` if any of the 6 files already exist).
2. **Features with priorities** — P0 = v1 must-have, P1 = v1 if time, P2 = later. If the user gave none, derive them from order and wording. Mark features you added yourself as « proposée » so the user sees them before accepting.
3. **Contradictions found, each with your proposed resolution** — e.g. "local-only data + external LLM → API key needs a small server proxy". Also check that the success metric can actually be measured by some feature; if not, propose the missing feature.
4. **Main assumptions** you will make.

Then ask "Je génère ?" via `AskUserQuestion` (Générer / Corriger quelque chose).

## Writing

1. Write in dependency order: PRD → TRD → AppFlow → DesignBrief → BackendSchema → ImplementationPlan. Reuse PRD feature names, entity names and screen names verbatim in every later doc.
2. Flag your own choices with `*(hypothèse)*` (`*(assumption)*` in English docs): per value when the user answered the rest of the section; once at the section heading when the whole section is yours (e.g. a DesignBrief after a skipped round 5).
3. PRD **Open questions**: numbered, each with your recommendation; include every assumption that changes scope, cost, architecture or data handling, plus the resolved contradictions. Cosmetic values (hex codes, px sizes) stay flagged in place only.
4. Scale to the audience: a solo/local tool gets no roles, no staging, no multi-region. When a template section doesn't apply (e.g. authorization without accounts), write one line saying why instead of a mechanical table.
5. Follow the project's own conventions if it has any (tracking files like CHANGES.md/TODOS.md, .gitignore rules).

## Verification (before announcing done)

Run with Python (`python3 -I`), not grep:
- all 6 files exist and are non-empty;
- no `{{` remains in any document;
- the **Traceability** table of ImplementationPlan.md has one row per P0 and P1 feature of the PRD, with non-empty Screens and Tasks cells, and every screen/entity named in it exists in AppFlow / BackendSchema;
- every entity in BackendSchema appears **by name** in the authorization section (matrix row, or listed in the one-line "no accounts" rule).

Names are matched exactly (whole cell item, not substring); entities are read from the `- **Name** —` lines of BackendSchema's Entities section.

First prove the checker catches failure: run it once on a copy with a `{{test}}` inserted and a feature row removed — it must fail. Then run it on the real docs. Fix gaps, then give the user: the file list, the top 3–5 open questions, and the suggested next step (step 1 of the implementation plan).

## Common mistakes

| Mistake | Fix |
|---|---|
| Asking all ~40 template fields one by one | 5 short rounds; derive the rest and flag as assumptions |
| Re-asking what free text already answered | Skip it; restate it in the confirmation instead |
| Resolving contradictory answers silently | Surface them in the confirmation with a proposed resolution |
| Success metric that no feature can measure | Propose the missing feature in the confirmation |
| Generic filler ("modern, clean UI", "fast") | Concrete values: hex colors, px sizes, ms targets, named screens |
| Feature names drifting between documents | Reuse PRD names verbatim; the traceability table exposes drift |
| Over-engineering a solo/local tool | Scale TRD and schema to the audience from round 2 |
