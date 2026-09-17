# Terminate Extracurricular Participant

> **Module:** `ssi_school_extracurricular`\
> **Model:** `school_extracurricular_participant`\
> **Menu:** School > Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - User`\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Open**.
- **Record:** **Leave Date** is filled in with a date on or after **Join Date** --
  Terminate fails with a _"Leave Date is empty or earlier than Join Date"_ error
  otherwise, and the record stays **Open**.
- **Config:** An active `policy.template` grants `terminate_ok` for state `open` to the
  actor's group.
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Participants** menu.
2. Open the record to terminate.
3. Fill in the **Leave Date** field.
4. Click **Save**.
5. Click the **Terminate** button.
6. In the wizard that appears, select the **Terminate Reason**.
7. Click **Confirm**.
8. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminated**.
- Only when Billing Mode is Charged to Enrollment: every addendum fee line billed
  through an allocated enrollment payment term that is not yet invoiced, and whose
  payment term has no Estimated Invoice Date or one later than the Leave Date, is
  removed. Addendum fee lines already linked to a customer invoice line are left
  untouched, whether or not the payment term is locked. Allocation lines themselves are
  kept, so a later Restart back to Open can recreate a removed line if the student
  rejoins before the new Leave Date.
- When Billing Mode is Separate Invoice or Free of Charge, only the state changes -- no
  addendum fee line exists to remove.
