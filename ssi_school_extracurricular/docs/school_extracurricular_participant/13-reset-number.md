# Reset Document Number — Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - Officer`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group `Extracurricular Participant - Officer`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**. Since this model only assigns a document number when
  the record transitions to **Open** (`_create_sequence_state = "open"`), a Draft
  record's number is already **/** in the common case; this action has no observable
  effect unless a document number was manually typed in beforehand.
