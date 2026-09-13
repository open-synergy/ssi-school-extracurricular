# Confirm Extracurricular Session

> **Module:** `ssi_school_extracurricular_session`\
> **Model:** `school_extracurricular_session`\
> **Menu:** School > Extracurricular > Extracurricular Session > Extracurricular
> Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `planned` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Planned**.
- **Record:** The **Journal** tab's **Journal - Material** and **Journal - Activity**
  are both filled in.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `planned` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (Monitor group, single level).
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Session > Extracurricular
   Sessions** menu.
2. Open the session to confirm.
3. Fill in the **Journal** tab's **Journal - Material** and **Journal - Activity**, if
   not already filled in.
4. Click the **Confirm** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Confirm**.
- An approval record is created for the Monitor group approval level.

> This is one of two paths to Done. The session may instead be marked Done directly
> (`05-done.md`) without going through this verification path.
