# Create Extracurricular Offering

> **Module:** `ssi_school_extracurricular_session`\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_offering`, aksi
> `01-create`

## Related Views

- **Sessions** smart button (`action_view_session`) on the Offering form's button box —
  opens the list of this offering's `school_extracurricular_session` records, in any
  status. Pure navigation; it does not write any field and does not change status. It
  carries no IK of its own.
- **Done Sessions** smart button (`action_view_session_done`) on the same button box —
  opens the list of this offering's sessions currently in **Done** status. Same as
  above: pure navigation, no field written, no IK of its own.
