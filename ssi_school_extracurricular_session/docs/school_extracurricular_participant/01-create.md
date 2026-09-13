# Create Extracurricular Participant

> **Module:** `ssi_school_extracurricular_session`\
> **Extends:** ssi_school_extracurricular — model `school_extracurricular_participant`, aksi
> `01-create`

## Related Views

- **Planned Sessions** smart button (`action_view_session_planned`) on the Participant
  form's button box — opens the sessions of this participant's Offering that are
  currently in **Planned** status. Pure navigation; it does not write any field and does
  not change status. It carries no IK of its own.
- **Done Sessions** smart button (`action_view_session_done`) on the same button box —
  opens the sessions of this participant's Offering that are currently in **Done**
  status. Same as above.
- **Present** smart button (`action_view_attendance_present`) on the same button box —
  opens this participant's attendance lines marked **Present**/**Late** on sessions that
  are currently in **Done** status. Same as above.
