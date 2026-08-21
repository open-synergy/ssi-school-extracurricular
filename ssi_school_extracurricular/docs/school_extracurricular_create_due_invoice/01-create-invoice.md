# Create Due Invoice — Extracurricular

> **Module:** ssi_school_extracurricular\
> **Model:** `school_extracurricular_create_due_invoice`\
> **Menu:** Extracurricular > Create Due Invoice\
> **Actor:** user in group `Extracurricular Participant - User`

## Pre-Condition

- **Data:** At least one Extracurricular Participant with **Billing Mode** = **Separate
  Invoice** has been opened (so it has generated a `school_extracurricular_payment_term`
  in status **Uninvoiced**) for the Student to be selected.
- **Data:** Every due, uninvoiced payment term for that Student shares the same
  Receivable Journal, Receivable Account, and Customer Invoice Type on their respective
  Offering — otherwise the wizard refuses to guess which one to use.
- **Access:** User is in group `Extracurricular Participant - User`.

## Flow

1. Open the **Extracurricular > Create Due Invoice** menu.
2. Fill in the required fields:
   - **Student** _(required)_: The student whose due payment terms will be consolidated.
   - **Invoice Date** _(required)_: Defaults to today.
   - **Due Date Until** _(required)_: Only uninvoiced payment terms whose Estimated Due
     Date is on or before this date are picked up. Also used as the Due Date of the
     resulting invoice.
3. The **Payment Terms** field is read-only and automatically lists every uninvoiced
   payment term of the selected Student due on or before Due Date Until.
4. Click the **Create Due Invoice** button.

## Post-Condition

- One `customer_invoice` document is created, consolidating one invoice line per detail
  line of every listed payment term.
- Each consolidated payment term is linked to the new invoice and is no longer
  Uninvoiced.
- If every involved Offering has **Auto Confirm Customer Invoice** enabled, the new
  invoice is automatically confirmed; otherwise it is left in Draft for manual review.
- The wizard dialog closes.
