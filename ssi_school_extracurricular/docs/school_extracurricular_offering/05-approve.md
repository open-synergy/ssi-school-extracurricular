# Approve Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - Officer`\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the pending approval level. The
  approval template for this model has a single level (Officer group), so any user in
  that group may approve.
- **Access:** User is in group `Extracurricular Offering - Officer`.

## Flow

1. Open the **Extracurricular > Extracurricular Offerings** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The single approval level is fulfilled, so status changes directly to **Open**. This
  transition is automatic (there is no separate "Open" button); it happens as soon as
  the approval completes.
