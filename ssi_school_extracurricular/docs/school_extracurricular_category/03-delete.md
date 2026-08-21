# Delete Extracurricular Category

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_category`\
> **Menu:** Extracurricular > Configuration > Categories\
> **Actor:** user in group `Extracurricular Category`\
> **Requires:** `01-create`

## Pre-Condition

- **Data:** No Extracurricular record uses this category (deleting a category still
  referenced by an extracurricular activity is rejected by the database).
- **Access:** User is in group `Extracurricular Category`.

## Flow

1. Open the **Extracurricular > Configuration > Categories** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
