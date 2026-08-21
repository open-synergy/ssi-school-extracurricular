# Confirm Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (Officer group, single level).
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- An approval record is created for the Officer group approval level.
