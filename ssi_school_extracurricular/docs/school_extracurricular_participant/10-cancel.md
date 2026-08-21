# Cancel Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - Officer`\
> **State:** `draft` | `confirm` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Open**.
- **Record:** When Billing Mode is Charged to Enrollment, every addendum fee line
  created on the allocated enrollment payment term(s) must still be unlocked — Cancel
  fails with _"An addendum fee line on the payment term is already locked"_ when any of
  them is already locked (meaning the enrollment has already been opened around it).
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `Extracurricular Participant - Officer`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- Every addendum fee line created on the allocated enrollment payment term(s) (only when
  Billing Mode is Charged to Enrollment, and none of them is locked) is removed, so the
  payment term's totals fall back to what they were before this participant was opened.
