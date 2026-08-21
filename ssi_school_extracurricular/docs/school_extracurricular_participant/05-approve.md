# Approve Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - Officer`\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** When **Billing Mode** is **Charged to Enrollment**, at least one
  **Allocation** line must already be set on the record — Approve fails with a _"Billing
  Mode is 'Charged to Enrollment' but no Allocation line is set"_ error otherwise, and
  the record stays **Waiting for Approval**. When Billing Mode is **Separate Invoice**
  or **Free of Charge**, no Allocation line is required.
- **Record:** The Offering's **Maximum Quota** (if greater than 0) must not already be
  reached by other participants in **Open** status on the same Offering — Approve fails
  with a quota error otherwise.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the pending approval level. The
  approval template for this model has a single level (Officer group), so any user in
  that group may approve.
- **Access:** User is in group `Extracurricular Participant - Officer`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The single approval level is fulfilled, so status changes directly to **Open**. This
  transition is automatic (there is no separate "Open" button); it happens as soon as
  the approval completes.
- One addendum fee line is created on each allocated enrollment payment term, mirroring
  the Allocation line's product, quantity, price, and taxes (only when Billing Mode is
  Charged to Enrollment).
