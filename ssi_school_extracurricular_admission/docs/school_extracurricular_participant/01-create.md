# Create Extracurricular Participant

> **Module:** `ssi_school_extracurricular_admission`\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_participant`, aksi
> `01-create`

## Additional Fields

When this module is installed and **Billing Mode** is set to **Charged to Admission**,
the create form gains two fields on page **Billing**:

- **Admission** _(required)_: The student's admission record used to bill this
  participant's fee. Must belong to the selected Student, and its academic term must
  match the selected Offering's academic term. Used instead of **Enrollment** for this
  Billing Mode — **Enrollment** is not required when Billing Mode is Charged to
  Admission.
- **Admission Allocation** _(required, at least one line)_: Admission payment term(s)
  this participant's fee is allocated to, replacing the **Allocation** field (which is
  hidden while Billing Mode is Charged to Admission). Only payment terms belonging to
  the selected Admission may be chosen. This is required before the participant can
  later be opened — see `05-approve`.

## Modified — Record Visibility

- The **Allocation** field (enrollment-mode allocation) is hidden on the form while
  Billing Mode is Charged to Admission; **Admission Allocation** is hidden otherwise.
  This is not a Flow step.
