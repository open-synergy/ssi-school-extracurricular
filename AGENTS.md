# Agent Instructions — ssi-school-extracurricular

This file is intended for **AI assistants** (GitHub Copilot, Claude, Cursor, ChatGPT,
and similar tools) working inside this repository.

This repository manages master data and transactions for extracurricular activities
offered by a school: activity categories, the activity catalog itself, term offerings,
participant enrollment, participant fee billing, and related payment terms.

---

## Modules in This Repository

| Module                                      | Description                                                                                                                                                |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ssi_school_extracurricular`                | Master data (category, extracurricular) and transactions (offering, participant, fee analysis, due invoice creation) for school extracurricular activities |
| `ssi_school_extracurricular_operating_unit` | Adds Operating Unit support to the Offering and Participant, and propagates it to the Route A addendum fee line and the Route B invoice                    |

---

## User Guide (Work Instructions)

Each module has a `docs/` directory containing **Work Instructions (IK)** — step-by-step
operational documentation for using the feature from the user's perspective.

### How to Answer User Questions About Feature Usage

1. Identify the feature being asked about.
2. Find the relevant Work Instruction from the index below.
3. **Read that file** before answering — do not fabricate steps from assumptions.
4. If a relevant extension module is installed (marked _additive_ below), also read its
   Work Instruction and **merge** it with the base IK.
5. Answer based on the content of the Work Instruction.

### Work Instruction Location Pattern

```
<module_name>/docs/<model_name>/<number>-<action>.md
```

---

## Work Instruction Index

### `ssi_school_extracurricular` — Model: `school_extracurricular_category`

Menu: **Extracurricular > Configuration > Categories**

| File                                                                           | Action                                |
| ------------------------------------------------------------------------------ | ------------------------------------- |
| `ssi_school_extracurricular/docs/school_extracurricular_category/01-create.md` | Create a new extracurricular category |
| `ssi_school_extracurricular/docs/school_extracurricular_category/02-edit.md`   | Edit an extracurricular category      |
| `ssi_school_extracurricular/docs/school_extracurricular_category/03-delete.md` | Delete an extracurricular category    |

### `ssi_school_extracurricular` — Model: `school_extracurricular`

Menu: **Extracurricular > Configuration > Extracurriculars**

| File                                                                  | Action                                |
| --------------------------------------------------------------------- | ------------------------------------- |
| `ssi_school_extracurricular/docs/school_extracurricular/01-create.md` | Create a new extracurricular activity |
| `ssi_school_extracurricular/docs/school_extracurricular/02-edit.md`   | Edit an extracurricular activity      |
| `ssi_school_extracurricular/docs/school_extracurricular/03-delete.md` | Delete an extracurricular activity    |

### `ssi_school_extracurricular` — Model: `school_extracurricular_offering`

Menu: **Extracurricular > Extracurricular Offerings**

| File                                                                                 | Action                                   |
| ------------------------------------------------------------------------------------ | ---------------------------------------- |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/01-create.md`       | Create a new extracurricular offering    |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/02-edit.md`         | Edit an extracurricular offering         |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/03-delete.md`       | Delete an extracurricular offering       |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/04-confirm.md`      | Confirm an extracurricular offering      |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/05-approve.md`      | Approve an extracurricular offering      |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/06-reject.md`       | Reject an extracurricular offering       |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/09-finish.md`       | Finish an extracurricular offering       |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/10-cancel.md`       | Cancel an extracurricular offering       |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/12-restart.md`      | Restart an extracurricular offering      |
| `ssi_school_extracurricular/docs/school_extracurricular_offering/13-reset-number.md` | Reset the document number of an offering |

### `ssi_school_extracurricular` — Model: `school_extracurricular_participant`

Menu: **Extracurricular > Extracurricular Participants**

| File                                                                                    | Action                                            |
| --------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/01-create.md`       | Create a new extracurricular participant          |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/02-edit.md`         | Edit an extracurricular participant               |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/03-delete.md`       | Delete an extracurricular participant             |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/04-confirm.md`      | Confirm an extracurricular participant            |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/05-approve.md`      | Approve an extracurricular participant (opens it) |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/06-reject.md`       | Reject an extracurricular participant             |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/09-finish.md`       | Finish an extracurricular participant             |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/10-cancel.md`       | Cancel an extracurricular participant             |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/12-restart.md`      | Restart an extracurricular participant            |
| `ssi_school_extracurricular/docs/school_extracurricular_participant/13-reset-number.md` | Reset the document number of a participant        |

### `ssi_school_extracurricular` — Model: `school_extracurricular_create_due_invoice`

Menu: **Extracurricular > Create Due Invoice**

| File                                                                                             | Action                                                       |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `ssi_school_extracurricular/docs/school_extracurricular_create_due_invoice/01-create-invoice.md` | Consolidate a student's due standalone fees into one invoice |

### `ssi_school_extracurricular_operating_unit` — Delta Work Instructions

These are **delta** documents: they only describe what changes on top of the base
module's own Work Instructions above (base module documents are the source of truth for
the rest of each Flow).

| File                                                                                                            | Extends                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `ssi_school_extracurricular_operating_unit/docs/school_extracurricular_offering/01-create.md`                   | `school_extracurricular_offering` — `01-create.md` (adds Operating Unit)                                                 |
| `ssi_school_extracurricular_operating_unit/docs/school_extracurricular_participant/01-create.md`                | `school_extracurricular_participant` — `01-create.md` (adds Operating Unit)                                              |
| `ssi_school_extracurricular_operating_unit/docs/school_extracurricular_create_due_invoice/01-create-invoice.md` | `school_extracurricular_create_due_invoice` — `01-create-invoice.md` (Operating Unit propagation and mismatch rejection) |

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the SSI Odoo development guidelines.
