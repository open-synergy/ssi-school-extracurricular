# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollmentPaymentTerm(models.Model):
    """Extends the payment term with extracurricular addendum billing.

    Adds ``extra_detail_ids`` -- the addendum fee lines coming from
    extracurricular participant allocations -- and folds their amount
    into the term's totals via ``amount_extra``. ``amount_untaxed``
    stays the sum of the regular ``detail_ids`` alone, so it keeps
    meaning "what the enrollment's own payment template billed";
    ``amount_extra`` is reported and totalled separately, and
    ``amount_total`` is the sum of both plus tax.
    """

    _inherit = "school_enrollment_payment_term"

    extra_detail_ids = fields.One2many(
        string="Extracurricular Addendum",
        comodel_name="school_enrollment_payment_term_extra_detail",
        inverse_name="term_id",
        help=(
            "Addendum fee lines billed through this payment term from "
            "extracurricular participants."
        ),
    )
    amount_extra = fields.Monetary(
        string="Extra Amount",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help=(
            "Total of the addendum fee lines, before tax, "
            "automatically computed from extra_detail_ids."
        ),
    )
    amount_tax_regular = fields.Monetary(
        string="Regular Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total tax amount of the regular detail lines only.",
    )
    amount_tax_extra = fields.Monetary(
        string="Extra Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total tax amount of the addendum fee lines only.",
    )

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "detail_ids.price_tax",
        "detail_ids.price_total",
        "extra_detail_ids",
        "extra_detail_ids.price_subtotal",
        "extra_detail_ids.price_tax",
        "extra_detail_ids.price_total",
    )
    def _compute_total(self):
        """Sum the detail and addendum lines into the term totals.

        ``amount_untaxed`` stays the sum of ``price_subtotal`` over
        ``detail_ids`` only. ``amount_extra`` is the sum of
        ``price_subtotal`` over ``extra_detail_ids``.
        ``amount_tax_regular``/``amount_tax_extra`` are the summed
        ``price_tax`` of each line set, and ``amount_tax`` is their
        total. ``amount_total`` is
        ``amount_untaxed + amount_extra + amount_tax``.

        :return: None
        """
        for record in self:
            amount_untaxed = amount_tax_regular = 0.0
            for detail in record.detail_ids:
                amount_untaxed += detail.price_subtotal
                amount_tax_regular += detail.price_tax
            amount_extra = amount_tax_extra = 0.0
            for extra in record.extra_detail_ids:
                amount_extra += extra.price_subtotal
                amount_tax_extra += extra.price_tax
            amount_tax = amount_tax_regular + amount_tax_extra
            record.amount_untaxed = amount_untaxed
            record.amount_extra = amount_extra
            record.amount_tax_regular = amount_tax_regular
            record.amount_tax_extra = amount_tax_extra
            record.amount_tax = amount_tax
            record.amount_total = amount_untaxed + amount_extra + amount_tax

    def _prepare_invoice_data(self):
        """Add the addendum fee lines to the invoice header create-vals.

        Extends the base header values with a ``line_ids`` key holding
        one ``(0, 0, vals)`` command per ``extra_detail_ids`` line, so
        they are created together with the ``customer_invoice`` header
        by ``_create_invoice``.

        :return: dict of ``customer_invoice`` values
        """
        self.ensure_one()
        result = super()._prepare_invoice_data()
        line_commands = [
            (0, 0, extra._prepare_invoice_line())  # pylint: disable=protected-access
            for extra in self.extra_detail_ids
        ]
        if line_commands:
            result["line_ids"] = line_commands
        return result

    def _create_invoice(self):
        """Create the invoice, then link back the addendum fee lines.

        Runs ``super()._create_invoice()`` first -- which also confirms
        the invoice when ``auto_confirm_customer_invoice`` is enabled
        -- then, for each ``extra_detail_ids`` line, finds the invoice
        line created from it (matched by ``extra_detail_id``) and
        writes it back onto ``customer_invoice_line_id``.

        :return: None
        """
        self.ensure_one()
        super()._create_invoice()
        invoice = self.customer_invoice_id
        for extra in self.extra_detail_ids:
            line = invoice.line_ids.filtered(
                lambda candidate, extra=extra: candidate.extra_detail_id == extra
            )
            if line:
                extra.write({"customer_invoice_line_id": line[0].id})
