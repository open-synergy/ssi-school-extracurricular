# Done — Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** School > Extracurricular > Extracurricular Session > Extracurricular
> Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `planned` → `done`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Planned**.
- **Config:** The session's Offering has two independent switches, **Track Participant
  Attendance** (default on) and **Track Instructor Attendance** (default off), each
  gating one of the conditions below. A session whose Offering has both switches off may
  be marked Done with no attendance recorded at all.
- **Record:** If the Offering's **Track Participant Attendance** is on, at least one
  attendance line exists on the **Attendance** tab — usually produced by
  `04-fill-attendance`, or added by hand.
- **Record:** If the Offering's **Track Instructor Attendance** is on, the
  **Instructors** tab is not empty and every line on it has its **Attendance** filled
  in.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Session > Extracurricular
   Sessions** menu.
2. Open the session to mark as done.
3. Click the **Done** button.

## Post-Condition

- Status changes to **Done**.
- Whichever of the session's attendance the Offering tracks -- participant, instructor,
  both, or neither -- is considered final.
