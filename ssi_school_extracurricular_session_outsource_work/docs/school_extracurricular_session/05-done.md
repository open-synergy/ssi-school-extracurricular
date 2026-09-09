# Done — Extracurricular Session

> **Module:** `ssi_school_extracurricular_session_outsource_work`\
> **Extends:** ssi_school_extracurricular_session — model `school_extracurricular_session`,
> aksi `05-done`

## Additional Pre-Condition

- **Data:** For every roster line on the **Instructors** tab whose **Attendance** is
  **Present** and whose person is an external **Contact** (not a school **Teacher**),
  the roster line's **Outsource Work Type** and **Outsource Work Usage** are filled, the
  Offering has an **Analytic Account**, and an **open** Outsource Work Rate exists for
  that person covering this session's date. Missing any of these blocks Done with a
  structured error instead of a silent skip.

## Modified Validation

- Done will fail **if** a present, externally-identified instructor roster line has no
  **Outsource Work Type**.
- Done will fail **if** a present, externally-identified instructor roster line has no
  **Outsource Work Usage**.
- Done will fail **if** the session's Offering has no **Analytic Account**.
- Done will fail **if** no **open** Outsource Work Rate covers that person on this
  session's date.

## Additional Post-Condition

- One **Outsource Work** honor document is created, in Draft, for every roster line on
  the **Instructors** tab whose **Attendance** is **Present** and whose person is an
  external **Contact** -- one document per person, visible on the new **Outsource Work
  Logs** tab. A roster line identified by a school **Teacher** instead of a Contact does
  not get one -- that honor is payroll, not accounts payable.
- A roster line that already has a non-cancelled honor document on this session (e.g.
  after Restart and Done again) does not get a second one.
- A session with no present, externally-identified instructor still reaches Done, with
  no Outsource Work Logs created.
