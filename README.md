# Vincent Lauriat — Toolkit

A personal collection of Claude Code plugins. Built as a hobby.

## Install

```shell
/plugin marketplace add vincentlauriat/toolkit
```

Then browse with `/plugin` or install directly:

```shell
/plugin install audit-report@vincentlauriat-toolkit
/plugin install marcel@vincentlauriat-toolkit
```

## Plugins

### `audit-report`

Generate exhaustive audit dossiers on any company, product, technology, or market — like a strategy consulting firm.

```shell
/audit-report Apple
/audit-report "marché des LLM" --lang fr
/audit-report OpenAI --depth full --swot --esg
/audit-report Notion --depth quick --brief
```

Produces a structured `audit-{subject}/` folder with up to 10 Markdown sections (history, market, technical, pricing, competition, financials, future outlook, ESG, SWOT, HR) plus machine-readable JSON artifacts (`_data.json`, `_sources.json`, `_manifest.json`).

**Options**: `--depth quick|full` · `--lang en|fr` · `--mode parallel|sequential|solo` · `--swot` · `--esg` · `--rh` · `--brief` · `--watch` · `--app-mode`

### `marcel` — Marcel, frame an app before coding

*Formerly `app-specs`. If you installed it, run `/plugin uninstall app-specs@vincentlauriat-toolkit`, then install `marcel`.*

Marcel speaks as a coach: he explains why each question matters and what each term means, in plain words. He speaks French, English, Brazilian Portuguese and European Portuguese, and writes the documents in any of them.

Frame an app — a new idea (greenfield) or an existing codebase (brownfield) — as a one-page overview plus six consistent documents written in `docs/specs/`.

- **Greenfield**: a short interview (four rounds, multiple-choice where possible), then the seven documents.
- **Brownfield**: reads the code first and asks only what the code cannot tell (goal, audience, out of scope, planned features). Every fact cites the file it was observed in, every feature is marked shipped or planned, contradictions with existing docs are listed (the code wins by default), and the implementation plan covers only the gap.
- **Update**: once specs exist, edits them in place — add a feature, record a technical change, resync with the code — and logs the revision.

```shell
/marcel "an app that suggests recipes from what's left in the fridge"   # greenfield
/marcel                                                                # brownfield, inside an existing repo
```

Produces `00-overview.md` (project presentation and document map, written last), `01-prd.md`, `02-trd.md`, `03-user-flows.md`, `04-design-brief.md`, `05-data-model.md` and `06-implementation-plan.md`. Unknown answers become flagged assumptions collected in the PRD's open questions; a traceability table links every priority feature to its screens, entities and tasks, and is checked before the skill reports done by a shipped script (`check.py`, with a self-test that proves it catches failures).

No terminal? Marcel can also be installed from Cowork in Claude Desktop, then used from the claude.ai chat or the iPhone app: see *Which device?* in the guide.

**User guide**: https://vincentlauriat.github.io/toolkit/marcel/ — what to prepare, a walkthrough of a session (new idea and existing codebase), how to read the result, building from the specs and keeping them up to date.

**Requires** `python3` for the checker. Optional: `mmdc` ([mermaid-cli](https://github.com/mermaid-js/mermaid-cli)) to render the Mermaid diagrams; without it they are only checked statically.
