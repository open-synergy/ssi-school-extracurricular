# Delete Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** and document number is **/**. Deleting a record whose
  status is not Draft, or whose document number has already been assigned, is rejected.
- **Data:** No Participant references this offering (deleting an offering still
  referenced by a participant is rejected by the database).
- **Access:** User is in group `Extracurricular Offering - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Offerings** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
