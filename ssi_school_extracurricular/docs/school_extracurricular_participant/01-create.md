# Create Extracurricular Participant

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_participant`\
> **Menu:** Extracurricular > Extracurricular Participants\
> **Actor:** user in group `Extracurricular Participant - User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** At least one **Extracurricular Offering** record exists (any status may be
  selected, but only an Offering that later reaches **Open** can accept new joiners in
  practice, since quota is checked on Open).
- **Data:** At least one **Student** record exists, with an **Enrollment** for the same
  Academic Term as the selected Offering.
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Participants** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Offering** _(required)_: The term's offering this participant is joining.
   - **Student** _(required)_: The student joining this extracurricular offering.
   - **Enrollment** _(required)_: The student's enrollment for the same academic term as
     the selected Offering.
   - **Join Date** _(required)_: The date this student joined. Defaults to today.
   - On the **Billing** tab: **Billing Mode**, **Product**, **Quantity**, and **Price
     Unit** are pre-filled from the selected Offering when Offering is chosen, but may
     be changed.
   - When **Billing Mode** is **Charged to Enrollment**, add at least one line under
     **Allocation** (page **Billing**), pointing to an enrollment payment term. This is
     required before the participant can later be opened — see `05-approve`.
   - When **Billing Mode** is **Separate Invoice**, the participant's own **Standalone
     Payment Term** lines (page **Standalone Payment Term**) may be added instead.
4. Click **Save**.

## Post-Condition

- A new Extracurricular Participant record is created in **Draft** status.
- The document number shows **/** until the record is opened.
