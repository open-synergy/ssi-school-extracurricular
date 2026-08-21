# Edit Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**. Editing a record while it is under the approval
  process is rejected with _"The operation is under approval process."_
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
