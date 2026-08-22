# Create Due Invoice — Extracurricular

> **Module:** ssi_school_extracurricular_operating_unit\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_create_due_invoice`,
> aksi `01-create-invoice`

## Additional Post-Condition

- The resulting `customer_invoice` carries the Operating Unit of the due payment terms'
  participants. This is not a Flow step -- it happens as a side effect of the existing
  **Create Due Invoice** button.

## Modified Validation

- **Create Due Invoice** will fail with an error if the due payment terms selected for
  consolidation come from extracurricular participants that do not all share the same
  Operating Unit, in addition to the base module's own Receivable Journal / Receivable
  Account / Customer Invoice Type check.
