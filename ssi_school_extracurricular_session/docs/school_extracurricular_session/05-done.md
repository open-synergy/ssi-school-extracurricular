# Done — Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** Extracurricular Session > Extracurricular Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `planned` → `done`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Planned**.
- **Record:** At least one attendance line exists on the **Attendance** tab — usually
  produced by `04-fill-attendance`, or added by hand.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **Extracurricular Session > Extracurricular Sessions** menu.
2. Open the session to mark as done.
3. Click the **Done** button.

## Post-Condition

- Status changes to **Done**.
- The session's attendance is considered final.
