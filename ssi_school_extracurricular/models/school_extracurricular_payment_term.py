# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolExtracurricularPaymentTerm(models.Model):
    """Represents one billing term of a standalone extracurricular fee.

    Route B billing (``billing_mode = "standalone"``) needs the
    participant to hold its own payment term(s), separate from the
    student's enrollment payment term -- so the extracurricular fee
    can be invoiced on its own schedule instead of riding along the
    enrollment invoice. Several terms, coming from different
    participants of the same student, may later be consolidated into
    one ``customer_invoice`` by the create-due-invoice wizard, which
    is why ``customer_invoice_id`` is N:1 rather than 1:1. The state
    is automatically computed: ``draft`` (participant still
    draft/confirm), ``uninvoiced`` (participant open/done, no
    customer invoice yet), ``invoiced`` (customer invoice created),
    ``manual`` (manually controlled), ``cancelled`` (participant
    cancelled/rejected).
    """

    _name = "school_extracurricular_payment_term"
    _description = "School Extracurricular Payment Term"
    _order = "sequence, id"

    @api.depends(
        "customer_invoice_id",
        "participant_id.state",
        "manually_control",
    )
    def _compute_state(self):
        """Derive the billing state from the participant and invoice.

        ``draft`` while the participant is in ``draft`` or
        ``confirm``. Once the participant is ``open`` or ``done`` the
        value becomes ``invoiced`` when ``customer_invoice_id`` is
        set, ``manual`` when ``manually_control`` is enabled, and
        ``uninvoiced`` otherwise. Any other participant state
        (cancelled, rejected) yields ``cancelled``.

        :return: None
        """
        for record in self:
            if record.participant_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.participant_id.state in ["open", "done"]:
                if record.customer_invoice_id:
                    state = "invoiced"
                elif record.manually_control:
                    state = "manual"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
        "detail_ids.price_tax",
        "detail_ids.price_total",
    )
    def _compute_total(self):
        """Sum the detail lines into the payment term totals.

        ``amount_untaxed``, ``amount_tax``, and ``amount_total`` are
        the sums of ``price_subtotal``, ``price_tax``, and
        ``price_total`` over ``detail_ids``; a term without detail
        lines totals zero.

        :return: None
        """
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for detail in record.detail_ids:
                amount_untaxed += detail.price_subtotal
                amount_tax += detail.price_tax
                amount_total += detail.price_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    participant_id = fields.Many2one(
        string="Extracurricular Participant",
        comodel_name="school_extracurricular_participant",
        required=True,
        ondelete="cascade",
        help="The extracurricular participant that owns this payment term.",
    )
    name = fields.Char(
        string="Term",
        required=True,
        help="Name of the billing period, e.g. 'Term 1 Fee'.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Order of the payment term within the participant. Lower "
        "values appear first.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="participant_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the participant.",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="school_extracurricular_payment_term_detail",
        inverse_name="term_id",
        copy=True,
        help="Product/fee detail lines within this payment term.",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total billing amount before tax, automatically computed "
        "from the detail lines.",
    )
    amount_tax = fields.Monetary(
        string="Tax",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total tax amount, automatically computed from the detail lines.",
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_total",
        store=True,
        currency_field="currency_id",
        help="Total billing amount including tax, automatically computed "
        "from the detail lines.",
    )
    customer_invoice_id = fields.Many2one(
        string="# Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        ondelete="restrict",
        help="The customer invoice this term was consolidated into. "
        "Several terms of different participants of the same student "
        "may point to the same invoice.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="Estimated date for issuing the invoice for this billing term.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="Estimated due date for payment of this billing term.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
        help="Billing status: Draft = participant still draft/confirm, "
        "Uninvoiced = participant open/done but no customer invoice yet, "
        "Invoiced = customer invoice created, "
        "Manually Controlled = managed manually, "
        "Cancelled = participant cancelled/rejected.",
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
        help="If enabled, this billing term is managed manually and does "
        "not require a customer invoice.",
    )
