# Create Extracurricular Category

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_category`\
> **Menu:** Extracurricular > Configuration > Categories\
> **Actor:** user in group `Extracurricular Category`

## Pre-Condition

- **Access:** User is in group `Extracurricular Category`.

## Flow

1. Open the **Extracurricular > Configuration > Categories** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: The name of the category, e.g. "Sport", "Art", "Science
     Club".
   - **Code**: Type a unique identifier, or leave it as **/** to skip assigning one.
   - **Sequence**: The display order of the category in lists. Defaults to **10** —
     lower values appear first.
4. Click **Save**.

## Post-Condition

- A new Extracurricular Category record is created and active.
