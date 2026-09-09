# Generate Extracurricular Sessions

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session_generate`\
> **Menu:** School > Extracurricular > Extracurricular Session > Generate Sessions\
> **Actor:** user in group `Extracurricular Session - User`

## Pre-Condition

- **Data:** At least one **Extracurricular Offering** record exists, with a Start Date
  and End Date the generated sessions' range must fall within.
- **Data:** At least one **Teacher** record exists, or at least one **Contact**
  (`res.partner`) to use as an External Coach.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Session > Generate Sessions**
   menu.
2. Fill in the required fields:
   - **Offering** _(required)_: The term's offering to generate sessions for.
   - **Start Date** _(required)_: Automatically filled from the selected Offering.
     Change if needed. Must not be earlier than the Offering's Start Date.
   - **End Date** _(required)_: Automatically filled from the selected Offering. Change
     if needed. Must not be later than the Offering's End Date.
   - **Start Time** _(required)_ and **End Time** _(required)_: The time applied to
     every generated session.
   - **Teacher** _(required if **External Coach** is empty)_: Automatically filled from
     the selected Offering's Teacher. Change if needed.
   - **External Coach** _(required if **Teacher** is empty)_: Automatically filled from
     the selected Offering's External Coach. Change if needed. Exactly one of
     **Teacher** or **External Coach** must be filled — clicking Generate is rejected
     otherwise, since every generated session carries this same rule.
   - **Location**: The location applied to every generated session. Optional.
3. In the **Weekdays** group, check at least one weekday — the wizard refuses to
   generate with none checked.
4. Click the **Generate** button.

## Post-Condition

- One **Planned** session is created for every date within the selected range whose
  weekday is checked, each carrying a copy of the Offering's Instructor roster (empty if
  the Offering's roster is empty). A candidate date that already has a session for the
  same Offering and Start Time is skipped, so running the wizard again with the same
  parameters does not duplicate sessions.
- No window is opened afterward; the wizard dialog closes. The generated sessions appear
  in the **Extracurricular Sessions** list once opened or refreshed.
