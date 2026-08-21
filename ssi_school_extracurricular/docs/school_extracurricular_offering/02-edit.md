# Edit Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**. Editing a record while it is under the approval
  process is rejected with _"The operation is under approval process."_
- **Access:** User is in group `Extracurricular Offering - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Offerings** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
