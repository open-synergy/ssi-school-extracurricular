# Create Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** Extracurricular Session > Extracurricular Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `—` → `planned`

## Pre-Condition

- **Data:** At least one **Extracurricular Offering** record exists, with a Start Date
  and End Date the session's Date must fall within.
- **Data:** At least one **Teacher** record exists.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **Extracurricular Session > Extracurricular Sessions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Offering** _(required)_: The term's offering this session is a meeting of.
   - **Extracurricular**, **School**, **Academic Term**: Automatically filled from the
     selected Offering.
   - **Teacher**: Automatically filled from the selected Offering's Teacher. Change if
     needed.
   - **Date** _(required)_: The date this session's meeting takes place. Must fall
     within the selected Offering's Start Date and End Date.
   - **Start Time** _(required)_ and **End Time** _(required)_: The time the meeting
     starts and ends. End Time must be later than Start Time.
   - **Location**: Where the meeting takes place. Optional.
   - **Topic**: A short label for what the meeting covers. Optional.
4. Click **Save**.

## Post-Condition

- A new record is created in **Planned** status.
