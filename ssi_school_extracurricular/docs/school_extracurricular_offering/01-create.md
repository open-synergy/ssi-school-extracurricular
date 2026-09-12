# Create Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** School > Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** At least one **Extracurricular** record exists.
- **Data:** At least one **Academic Year** and one **Academic Term** (belonging to that
  year) exist.
- **Data:** At least one **Teacher** record exists, or at least one **Contact**
  (`res.partner`) to use as an External Coach.
- **Access:** User is in group `Extracurricular Offering - User`.

## Flow

1. Open the **School > Extracurricular > Extracurricular Offerings** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Extracurricular** _(required)_: The extracurricular activity being opened this
     term. Selecting it derives **Teacher** and **External Coach** from the
     Extracurricular's own defaults, when set.
   - **Academic Year** _(required)_: The academic year this offering runs in.
   - **Academic Term** _(required)_: The academic term this offering runs in. Must
     belong to the selected Academic Year.
   - **Teacher** _(required if **External Coach** is empty)_: The coach/teacher in
     charge of this term's offering, when the coach is a school employee.
   - **External Coach** _(required if **Teacher** is empty)_: The external coach (person
     or institution, not a school employee) in charge of this term's offering. Exactly
     one of **Teacher** or **External Coach** must be filled; filling both, or leaving
     both empty, is rejected on Save.
   - **Start Date** _(required)_: The date this term's offering starts running.
   - **End Date** _(required)_: The date this term's offering ends running. Must not be
     earlier than Start Date.
   - **Currency** _(required)_: The currency used for this offering's fee. Defaults to
     the company currency.
   - **Product** _(required)_: The product used to bill this offering's fee. Defaults
     from the selected Extracurricular's default Product.
   - **Billing Mode** _(required)_: How the fee is billed — Charged to Enrollment,
     Separate Invoice, or Free of Charge. Defaults to Charged to Enrollment.
   - **Billing Frequency** _(required)_: How often the fee is billed — One Time or Every
     Payment Term. Defaults to One Time.
   - On the **Quota** tab: **Minimum Quota** and **Maximum Quota**. A Maximum Quota of 0
     means no upper limit.
   - On the **Billing** tab: **Price Unit** _(required)_ and, when Billing Mode is
     Separate Invoice, **Customer Invoice Type**, **Receivable Journal**, and
     **Receivable Account**.
   - On the **Groups** tab _(optional)_: add one or more **Group** lines to split this
     offering into batches, each with its own quota and coach(es) -- useful when one
     activity runs as several classes (e.g. "Mini Soccer 1", "Mini Soccer 2"). Leave
     this tab empty when the offering runs as a single batch. Each Group line requires
     **Name** _(required)_; **Code**, **Teachers**, and **Maximum Quota** are optional.
     A Group's **Maximum Quota** of 0 means no upper limit for that Group, independent
     of the offering's own Maximum Quota.
4. Click **Save**.

## Post-Condition

- A new Extracurricular Offering record is created in **Draft** status.
- The document number shows **/** until the record is opened.
