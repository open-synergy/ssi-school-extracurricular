# Restart Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** Extracurricular Session > Extracurricular Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `done` | `cancelled` → `planned`\
> **Requires:** `05-done`

## Pre-Condition

- **Record:** Status is **Done** or **Cancelled**.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **Extracurricular Session > Extracurricular Sessions** menu.
2. Open the session to restart.
3. Click the **Restart** button.

## Post-Condition

- Status returns to **Planned**.
- Any recorded **Cancel Reason** is cleared.
