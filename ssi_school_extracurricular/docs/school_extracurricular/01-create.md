# Create Extracurricular

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular`\
> **Menu:** Extracurricular > Configuration > Extracurriculars\
> **Actor:** user in group `Extracurricular`

## Pre-Condition

- **Data:** At least one **Extracurricular Category** record exists.
- **Data:** At least one **School** record exists.
- **Access:** User is in group `Extracurricular`.

## Flow

1. Open the **Extracurricular > Configuration > Extracurriculars** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: The name of the extracurricular activity.
   - **Code**: Type a unique identifier, or leave it as **/** to skip assigning one.
   - **Category** _(required)_: The category this activity belongs to.
   - **School** _(required)_: The school that offers this activity.
   - **Allowed Grades**: The grades allowed to join this activity. Leave empty to allow
     every grade, not to allow none.
   - **Teacher**: The default coach/teacher in charge of this activity. Optional.
   - **Product**: The default product used to bill the fee of this activity. Optional.
4. Click **Save**.

## Post-Condition

- A new Extracurricular record is created and active.
