# Delete Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** and document number is **/**. Deleting a record whose
  status is not Draft, or whose document number has already been assigned, is rejected.
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
