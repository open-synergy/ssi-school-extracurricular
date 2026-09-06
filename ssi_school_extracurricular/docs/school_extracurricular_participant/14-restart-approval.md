# Restart Approval Process — Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** School > Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - Officer`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**, and the record currently has no
  approval template assigned (for example, because no `approval.template` matched at the
  time of Confirm, or the previously matching template was later deactivated).
- **Config:** An active `policy.template` for this model grants `restart_approval_ok`
  for state `confirm` to the actor's group, and only while the record has no approval
  template assigned.
- **Config:** An active `approval.template` for this model now matches this record, with
  an approver group configured for its approval level, so the process can be rebuilt
  once restarted.
- **Access:** User is in group `Extracurricular Participant - Officer`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Participants** menu.
2. Open the record whose approval process is stalled.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status remains **Waiting for Approval**.
- A new approval process is created from the approval template that now matches the
  record.
