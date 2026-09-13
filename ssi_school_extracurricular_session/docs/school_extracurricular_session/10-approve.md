# Approve Extracurricular Session

> **Module:** `ssi_school_extracurricular_session`\
> **Model:** `school_extracurricular_session`\
> **Menu:** School > Extracurricular > Extracurricular Session > Extracurricular
> Sessions\
> **Actor:** user in group `Extracurricular Session - Monitor`\
> **State:** `confirm` → `done` (Approve) or `confirm` → `reject` (Reject)\
> **Requires:** `09-confirm`

## Pre-Condition

- **Record:** Status is **Confirm**.
- **Config:** An active `policy.template` grants `approve_ok`/`reject_ok` to the actor's
  group.
- **Access:** User is registered as an approver on the pending approval level. The
  approval template for this model has a single level (Monitor group), so any user in
  that group may approve or reject.
- **Access:** User is in group `Extracurricular Session - Monitor`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Session > Extracurricular
   Sessions** menu.
2. Open the session to verify.
3. On the **Monitoring** tab, check **Coach Present** if the coach in charge of this
   session actually attended the meeting. If not checked, fill in **Monitoring Note**
   explaining why the meeting still counts as held -- Approve is rejected if **Coach
   Present** is unchecked and **Monitoring Note** is empty.
4. Click the **Approve** button to verify the meeting as held, or the **Reject** button
   to dispute it.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- **Approve:** The single approval level is fulfilled, so status changes directly to
  **Done**. This transition is automatic (there is no separate "Done" button on this
  path); it happens as soon as the approval completes.
- **Reject:** Status changes to **Reject**, and the Monitor's rejection is recorded on
  the session's chatter.

> **Restart Approval Process:** If the approval template no longer matches this record
> (e.g. it was deactivated while this session was in Confirm), the **Restart Approval
> Process** button appears to a Monitor, letting them reload it once a matching template
> is available again.
