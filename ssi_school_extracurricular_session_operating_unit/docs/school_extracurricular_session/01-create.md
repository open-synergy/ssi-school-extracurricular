# Create Extracurricular Session

> **Module:** ssi_school_extracurricular_session_operating_unit\
> **Extends:** ssi_school_extracurricular_session — model `school_extracurricular_session`,
> aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one read-only field:

- **Operating Unit**: The operating unit this session belongs to. Automatically filled
  from the selected Offering's own Operating Unit, alongside Extracurricular, School,
  and Academic Term. Cannot be edited directly — if the Offering's Operating Unit
  changes later, every one of its sessions changes with it.

## Modified — Record Visibility

- The Extracurricular Session list is now filtered by operating unit for users in the
  `Operating Unit` group (implied by the `Manager` group). A user only sees sessions
  whose Operating Unit is one of their own assigned operating units. This is not a Flow
  step.
