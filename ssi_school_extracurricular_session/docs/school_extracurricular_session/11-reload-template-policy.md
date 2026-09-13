# Reload Template Policy — Extracurricular Session

> **Module:** `ssi_school_extracurricular_session`\
> **Model:** `school_extracurricular_session`\
> **Menu:** School > Extracurricular > Extracurricular Session > Extracurricular
> Sessions\
> **Actor:** administrator in group `Settings / Technical Settings`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** None — usable in any state.
- **Config:** At least one active `policy.template` exists for this model, so a matching
  template can be found.
- **Access:** User is in group `Settings / Technical Settings` (`base.group_system`).
  The **Policies** tab that contains this button is only visible to this group.

## Flow

1. Open the **School > Extracurricular > Extracurricular Session > Extracurricular
   Sessions** menu.
2. Open the record whose assigned policy template should be re-evaluated.
3. On the **Policies** tab, click **Reload Template Policy**.

## Post-Condition

- **Policy Template** is recomputed and re-assigned to the highest-sequence
  `policy.template` for this model whose condition currently matches the record. This
  may change which policy fields (`confirm_ok`, `approve_ok`, `reject_ok`,
  `restart_approval_ok`) are granted, without changing the record's `state`.
