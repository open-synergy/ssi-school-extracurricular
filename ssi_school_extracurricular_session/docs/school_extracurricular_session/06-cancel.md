# Cancel Extracurricular Session

> **Module:** ssi_school_extracurricular_session\
> **Model:** `school_extracurricular_session`\
> **Menu:** Extracurricular Session > Extracurricular Sessions\
> **Actor:** user in group `Extracurricular Session - User`\
> **State:** `planned` → `cancelled`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Planned**.
- **Access:** User is in group `Extracurricular Session - User`.

## Flow

1. Open the **Extracurricular Session > Extracurricular Sessions** menu.
2. Open the session to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, fill in the **Cancel Reason** _(required)_ — the wizard
   refuses to confirm an empty reason.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
- The **Cancel Reason** is recorded on the session and shown on the **Description** tab.
