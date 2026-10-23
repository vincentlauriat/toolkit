# Document templates

Section headings for each file. `{{...}}` marks a placeholder to replace — never copy `{{` into a document. Translate headings to the documents' language. Fill every section with concrete content; when a section does not apply (e.g. no auth for a solo local tool), write one line saying so and why — never delete it silently.

---

## 0. 00-overview.md — Project overview

Goal: let a newcomer understand the project in two minutes and know where to read next. Written **last**; it summarises the other documents and introduces no new fact. Maximum one page.

- **Name and pitch** — product name, one sentence on what it does and for whom.
- **Problem and goal** — the pain point and the measurable success signal, copied from the PRD.
- **Status** — new, shipped (version, date) or in progress; one line.
- **Key choices** — platform, stack, hosting, data and access model, in 4–6 bullets taken from the TRD and the data model.
- **Document map** — table: file | what you will find | read it when. One row per document `01-` to `06-`, each file name written exactly as on disk (the checker looks for them).
- **Top open questions** — the 3–5 most important from the PRD, with the recommended answer.
- **Next step** — step 1 of the implementation plan.

---

## 1. 01-prd.md — Product Requirements Document

Goal: define what the product must do and how success is measured.

- **Product name and one-line pitch** — name + the problem it solves.
- **Target users** — who they are, what they need (1–3 personas max).
- **Problem and current solution** — the pain point and what users do today.
- **Goal and success metric** — the intended outcome and one measurable signal (number + timeframe).
- **Main features** — table: feature | user benefit | priority (P0/P1/P2).
- **Out of scope for v1** — what waits, and why.
- **User stories** — "As a {{user}}, I want {{action}}, so that {{outcome}}." At least one per P0 and P1 feature.
- **Acceptance criteria** — "Given {{starting situation}}, when {{action}}, then {{visible result}}." At least one per user story.
- **Risks and dependencies** — table: risk | likelihood (low/med/high) | impact | mitigation or fallback. Cover product risks (adoption), technical risks (external API, data quality) and dependencies (third parties, people, deadlines).
- **Open questions** — numbered decisions the product owner must still make, each with a recommendation. Includes every assumption flagged in the other documents.
- **Revision log** — table: date | change | documents touched. First row: initial version. Update mode appends a row per revision.

---

## 2. 02-trd.md — Technical Requirements Document

Goal: make technical choices explicit so the build does not rest on guesses.

- **Platforms** — web, iOS, Android, macOS, other; minimum OS/browser versions.
- **Frontend and hosting** — framework, runtime, deployment target.
- **Backend and database** — services, data storage, region.
- **Authentication and roles** — sign-in methods, permissions.
- **External services and APIs** — table: provider | usage | limits/quotas | who owns the credentials.
- **Architecture** — main components and how data flows (a Mermaid diagram is welcome; `check.py` validates its syntax statically).
- **Security and privacy** — sensitive data, access controls, retention period.
- **Performance and reliability targets** — response times (ms), availability, backups.
- **Testing strategy** — levels (unit, integration, end-to-end, manual), tools, what is deliberately not tested, the checks that gate a release (CI).
- **Run cost** — table: item (hosting, database, each external API) | unit price or quota | expected monthly cost at the audience's scale. Order of magnitude, basis stated, flagged as a hypothesis; one line for a local tool.
- **Environments and release** — development, staging, production, CI/CD.
- **Key technical decisions and trade-offs** — table: choice | reason | alternative considered.

---

## 3. 03-user-flows.md — User flows

Goal: show every screen, every user path, and what happens on each click.

- **Entry points** — how the user arrives (URL, install, deep link, notification…).
- **Screen list** — table: screen | purpose | data needed.
- **Main path** — `{{start screen}} -> {{action}} -> {{next screen}} -> {{success state}}`.
- **Alternative paths** — cancel, edit, go back, skip.
- **Action details** — for each action: trigger, validation, loading state, success state, error state, next screen (a table per screen works well).
- **Navigation rules** — tabs, back-button behavior, deep links.
- **Empty and blocked states** — no data, permission denied, offline.
- **First use** — onboarding and account creation.

---

## 4. 04-design-brief.md — UI/UX design brief

Goal: give the app a coherent, easy-to-use visual direction.

- **Audience and tone** — who it is for, three adjectives describing the design.
- **Reference products** — links, and what to borrow or avoid from each.
- **Color palette** — primary, accent, background, text, status colors (success/warning/error/info), with hex values; light and dark if relevant.
- **Typography** — font(s), heading and body sizes (px/pt), weights.
- **Components** — buttons, forms, cards, navigation, alerts: variants and rules.
- **Layout rules** — grid, spacing scale, responsive breakpoints.
- **Per-screen notes** — key content and hierarchy for each screen listed in UserFlows.
- **Accessibility** — contrast (WCAG AA minimum), keyboard navigation, labels, touch target size (≥44 px).
- **Interaction states** — hover, focus, disabled, loading, error, success.
- **Required assets** — logo, icons (set/library), illustrations, screenshots.

---

## 5. 05-data-model.md — Data model

Goal: define stored data, how it links, and who can access it.

- **Entities** — one line per entity, in the exact format `- **EntityName** — what it represents.` (the verification parses this). A boolean or small attribute (e.g. a favorite flag) is a field, not an entity.
- **Tables / collections** — for each: name; fields and types; required fields; default values; indexes (a table per entity).
- **Relations** — one-to-one, one-to-many, many-to-many, foreign keys (an ER diagram in Mermaid is welcome).
- **Data ownership** — which records belong to which users or teams.
- **Authentication flow** — sign-up, sign-in, reset, session duration.
- **Authorization rules** — matrix: entity × role → read / create / update / delete. Without accounts: one line stating that the single local user has full access to all entities, **naming each entity**, and why that is acceptable.
- **Data validation** — lengths, formats, uniqueness, business rules.
- **Retention and deletion** — what is kept, deleted, exportable (GDPR if applicable).
- **Migrations and seed data** — initial data and the process for schema changes.

---

## 6. 06-implementation-plan.md — Implementation plan

Goal: give the AI agent a build order with checkpoints.

- **Step 1, project setup** — repo, environment, dependencies, deployment.
- **Step 2, data and authentication** — schema, migrations, permissions, tests.
- **Step 3, main user path** — screens and API work in dependency order.
- **Step 4, secondary features** — the rest of the PRD.
- **Step 5, quality** — error handling, accessibility, security, performance.
- **Step 6, go-live** — test plan, deployment, rollback, monitoring.

Under each step heading, give an **estimated effort** (order of magnitude in days or sessions, flagged as a hypothesis). For each task, a table row: task | owner or agent | inputs | deliverable | done criterion | depends on.

In existing-project mode, steps cover only the gap between the code and the PRD; shipped features appear in the traceability table with `existant : path` in Tasks.

**Traceability** (required, at the end) — one row per P0 and P1 feature, names copied verbatim from the PRD:

Several screens, entities or tasks in one cell are separated by `, ` and written with their exact names.

| Feature | Priority | Screens (UserFlows) | Entities (DataModel, or "—" if none stored) | Tasks |
|---|---|---|---|---|

End each step with a **checkpoint**: run the app, check the acceptance criteria covered by this step, record any unresolved issue before moving on.
