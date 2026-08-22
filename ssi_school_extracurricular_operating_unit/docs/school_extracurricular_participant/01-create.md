# Create Extracurricular Participant

> **Module:** ssi_school_extracurricular_operating_unit\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_participant`, aksi
> `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field:

- **Operating Unit**: The operating unit this participant's fee belongs to.
  Automatically copied from the selected **Offering**'s own Operating Unit as soon as an
  Offering is picked, but may be changed afterwards -- a participant's fee can be billed
  to an operating unit different from its Offering's.

## Additional Post-Condition

- When this participant is opened (see the base module's `05-approve.md`, which
  transitions the document to `open`), every addendum fee line this module's base
  Post-Condition creates on the enrollment's payment term (Route A) carries this
  participant's own Operating Unit. This is not a Flow step -- it happens as a side
  effect of the existing Approve action.
- When this participant's fee is later consolidated into an invoice by the **Create Due
  Invoice** wizard (Route B), the resulting invoice carries this participant's Operating
  Unit -- see `docs/school_extracurricular_create_due_invoice/01-create-invoice.md` in
  this module.

## Modified — Record Visibility

- The Extracurricular Participant list is now filtered by operating unit for users in
  the `Operating Unit` group (implied by the `Manager` group). A user only sees
  participants whose Operating Unit is one of their own assigned operating units. This
  is not a Flow step.
