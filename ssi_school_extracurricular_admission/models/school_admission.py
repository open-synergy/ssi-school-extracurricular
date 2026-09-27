# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolAdmission(models.Model):
    """Extends the admission to fold in extracurricular addendum lines.

    ``product_summary_ids`` now also covers
    ``school_admission_payment_term_extra_detail`` rows, so
    extracurricular fees charged to admission show up in the same
    product summary as the admission's own payment template lines.
    """

    _inherit = "school_admission"

    def _recompute_product_summary(self):
        """Fold the addendum fee lines into the product summary.

        Runs ``super()`` first, which rebuilds ``product_summary_ids``
        from ``payment_term_ids.detail_ids`` alone, then merges every
        ``extra_detail_ids`` line into the resulting summary per
        product -- adding to an existing summary row when the product
        already has one, or creating a new row otherwise.

        :return: None
        """
        super()._recompute_product_summary()  # pylint: disable=protected-access
        Summary = self.env[  # pylint: disable=invalid-name
            "school_admission_product_summary"
        ]
        for record in self.sudo():
            extra_data = {}
            for term in record.payment_term_ids:
                for extra in term.extra_detail_ids:
                    pid = extra.product_id.id
                    if not pid:
                        continue
                    if pid not in extra_data:
                        extra_data[pid] = {
                            "amount_untaxed": 0.0,
                            "amount_tax": 0.0,
                            "amount_total": 0.0,
                        }
                    extra_data[pid]["amount_untaxed"] += extra.price_subtotal
                    extra_data[pid]["amount_tax"] += extra.price_tax
                    extra_data[pid]["amount_total"] += extra.price_total
            if not extra_data:
                continue
            existing = {
                summary.product_id.id: summary for summary in record.product_summary_ids
            }
            for pid, data in extra_data.items():
                if pid in existing:
                    summary = existing[pid]
                    summary.write(
                        {
                            "amount_untaxed": summary.amount_untaxed
                            + data["amount_untaxed"],
                            "amount_tax": summary.amount_tax + data["amount_tax"],
                            "amount_total": summary.amount_total + data["amount_total"],
                        }
                    )
                else:
                    data["admission_id"] = record.id
                    data["product_id"] = pid
                    Summary.create(data)
