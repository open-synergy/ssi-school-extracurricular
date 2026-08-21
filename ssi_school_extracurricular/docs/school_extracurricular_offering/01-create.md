# Create Extracurricular Offering

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_offering`\
> **Menu:** Extracurricular > Extracurricular Offerings\
> **Actor:** user in group `Extracurricular Offering - User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** At least one **Extracurricular** record exists.
- **Data:** At least one **Academic Year** and one **Academic Term** (belonging to that
  year) exist.
- **Data:** At least one **Teacher** record exists.
- **Access:** User is in group `Extracurricular Offering - User`.

## Flow

1. Open the **Extracurricular > Extracurricular Offerings** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Extracurricular** _(required)_: The extracurricular activity being opened this
     term.
   - **Academic Year** _(required)_: The academic year this offering runs in.
   - **Academic Term** _(required)_: The academic term this offering runs in. Must
     belong to the selected Academic Year.
   - **Teacher** _(required)_: The coach/teacher in charge of this term's offering.
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
4. Click **Save**.

## Post-Condition

- A new Extracurricular Offering record is created in **Draft** status.
- The document number shows **/** until the record is opened.
