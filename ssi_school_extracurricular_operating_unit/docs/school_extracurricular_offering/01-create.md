# Create Extracurricular Offering

> **Module:** ssi_school_extracurricular_operating_unit\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_offering`, aksi
> `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field:

- **Operating Unit**: The operating unit this offering belongs to. Defaults to the
  current user's default operating unit, but may be changed. Every extracurricular
  participant who later joins this offering copies this value when the offering is
  selected (see the participant's own `01-create.md` delta).

## Modified — Record Visibility

- The Extracurricular Offering list is now filtered by operating unit for users in the
  `Operating Unit` group (implied by the `Manager` group). A user only sees offerings
  whose Operating Unit is one of their own assigned operating units. This is not a Flow
  step.
