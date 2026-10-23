# Vincent Lauriat — Toolkit

A personal collection of Claude Code plugins. Built as a hobby.

## Install

```shell
/plugin marketplace add vincentlauriat/toolkit
```

Then browse with `/plugin` or install directly:

```shell
/plugin install audit-report@vincentlauriat-toolkit
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

### `app-specs`

Frame an app before coding: a short interview (four rounds, multiple-choice where possible), then a one-page overview plus six consistent documents written in `docs/specs/`. It also works on an existing codebase (documents what the code does) and can update existing specs in place.

```shell
/app-specs
/app-specs "an app that suggests recipes from what's left in the fridge"
```

Produces `00-overview.md` (project presentation and document map, written last), `01-prd.md`, `02-trd.md`, `03-user-flows.md`, `04-design-brief.md`, `05-data-model.md` and `06-implementation-plan.md`. Unknown answers become flagged assumptions collected in the PRD's open questions; a traceability table links every priority feature to its screens, entities and tasks, and is checked before the skill reports done by a shipped script (`check.py`, with a self-test that proves it catches failures).
