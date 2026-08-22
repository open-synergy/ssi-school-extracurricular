# Fill Attendance — Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** Extracurricular Session > Extracurricular Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Planned**. The **Fill Attendance** button is only available in
  this status.
- **Data:** At least one Participant of the session's Offering is in status **Open**,
  joined on or before the session's Date, and has not left before that Date.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **Extracurricular Session > Extracurricular Sessions** menu.
2. Open the session to fill attendance for.
3. Click the **Fill Attendance** button.

## Post-Condition

- One **Present** attendance line is created on the **Attendance** tab for every active
  Participant of the session's Offering that does not already have a line on this
  session. A Participant that already has a line is skipped, so the button may be
  clicked again without duplicating lines.
- Attendance lines may still be added, changed, or removed by hand on the **Attendance**
  tab.
