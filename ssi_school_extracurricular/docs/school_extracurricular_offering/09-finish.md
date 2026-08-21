# Finish Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - User`\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Open**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group `Extracurricular Offering - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Offerings** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
