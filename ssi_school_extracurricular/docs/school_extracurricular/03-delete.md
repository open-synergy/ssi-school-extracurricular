# Delete Extracurricular

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular`\
> **Menu:** School > Configuration > Extracurricular > Extracurriculars\
> **Actor:** user in group `Extracurricular`\
> **Requires:** `01-create`

## Pre-Condition

- **Data:** No offering references this extracurricular activity (deleting an
  extracurricular activity still referenced by an offering is rejected by the database).
- **Access:** User is in group `Extracurricular`.

## Flow

1. Open the **School > Configuration > Extracurricular > Extracurriculars** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
