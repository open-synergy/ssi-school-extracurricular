# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SchoolExtracurricularFeeAnalysis(models.Model):
    """Read-only reporting model that flattens extracurricular fee lines.

    Extracurricular fees are billed through two different routes: an
    addendum on the student's enrollment payment term (Route A,
    ``school_enrollment_payment_term_extra_detail``) or the
    participant's own standalone payment term (Route B,
    ``school_extracurricular_payment_term_detail``). Neither table
    alone answers "how much did we bill per extracurricular, per
    category, per grade, per semester" -- this view ``UNION ALL``\\ s
    both sources into one row axis, tagged with ``billing_route``, for
    pivot-table analysis. Backed by a plain SQL view, not stored;
    always reflects current data.
    """

    _name = "school_extracurricular_fee_analysis"
    _description = "Extracurricular Fee Analysis"
    _auto = False
    _order = "id desc"

    billing_route = fields.Selection(
        string="Billing Route",
        selection=[
            ("enrollment", "Charged to Enrollment"),
            ("standalone", "Separate Invoice"),
        ],
        readonly=True,
        help=(
            "Which billing route this fee line came from: Charged to "
            "Enrollment (an addendum on the student's enrollment "
            "payment term) or Separate Invoice (the participant's own "
            "standalone payment term)."
        ),
    )
    participant_id = fields.Many2one(
        string="Participant",
        comodel_name="school_extracurricular_participant",
        readonly=True,
        help="The extracurricular participant this fee line was billed from.",
    )
    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        readonly=True,
        help="The term's offering the participant joined.",
    )
    extracurricular_id = fields.Many2one(
        string="Extracurricular",
        comodel_name="school_extracurricular",
        readonly=True,
        help="The extracurricular activity being billed.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="school_extracurricular_category",
        readonly=True,
        help="The category of the extracurricular activity.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        readonly=True,
        help="The student being billed, taken from the participant.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        help="The student's contact partner, taken from the participant.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        help="The school running the offering the participant joined.",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        readonly=True,
        help="The company that owns the school of the offering.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        help="The academic year of the joined offering.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        readonly=True,
        help="The academic term of the joined offering.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        readonly=True,
        help="The coach/teacher in charge of the joined offering.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        readonly=True,
        help="The product/fee type billed on this line.",
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        readonly=True,
        help="The category of the billed product.",
    )
    customer_invoice_id = fields.Many2one(
        string="Customer Invoice",
        comodel_name="customer_invoice",
        readonly=True,
        help="The customer invoice linked to the owning payment term, if generated.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        readonly=True,
        help="The billing currency of the fee line.",
    )
    uom_quantity = fields.Float(
        string="Qty",
        readonly=True,
        help="Quantity billed on the fee line.",
    )
    price_unit = fields.Monetary(
        string="Unit Price",
        currency_field="currency_id",
        readonly=True,
        help="Unit price of the fee line.",
    )
    price_subtotal = fields.Monetary(
        string="Untaxed",
        currency_field="currency_id",
        readonly=True,
        help="Untaxed subtotal of the fee line.",
    )
    price_tax = fields.Monetary(
        string="Tax",
        currency_field="currency_id",
        readonly=True,
        help="Tax amount of the fee line.",
    )
    price_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        readonly=True,
        help="Total amount (including tax) of the fee line.",
    )

    def init(self):
        """Create the SQL view that backs this analysis model.

        Odoo calls this on every module install or update for an
        ``_auto = False`` model. The existing view is dropped first and
        recreated from ``_select_query``, so a changed query takes
        effect as soon as the module is updated.

        :return: None
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE VIEW %s AS (%s)""" % (self._table, self._select_query())
        )

    def _select_query(self):
        """Return the SQL SELECT that feeds the analysis view.

        ``UNION ALL``\\ s Route A
        (``school_enrollment_payment_term_extra_detail``) and Route B
        (``school_extracurricular_payment_term_detail``) fee lines
        into one row axis. Row ``id`` is derived as ``detail.id * 2``
        for Route A and ``detail.id * 2 + 1`` for Route B so the two
        sources never collide; ``row_number()`` is deliberately not
        used because its value is not stable across refreshes.
        Extension point: override to add columns or joins; every added
        column must be matched by a field declared on this model and
        present, in the same position, on both branches of the
        ``UNION ALL``.

        :return: str containing the SELECT statement
        """
        return """
            SELECT
                (detail.id * 2) AS id,
                'enrollment' AS billing_route,
                detail.participant_id AS participant_id,
                participant.offering_id AS offering_id,
                offering.extracurricular_id AS extracurricular_id,
                offering.category_id AS category_id,
                participant.student_id AS student_id,
                participant.partner_id AS partner_id,
                participant.school_id AS school_id,
                sch.company_id AS company_id,
                participant.academic_year_id AS academic_year_id,
                participant.academic_term_id AS academic_term_id,
                offering.teacher_id AS teacher_id,
                detail.product_id AS product_id,
                detail.product_category_id AS product_category_id,
                term.customer_invoice_id AS customer_invoice_id,
                detail.currency_id AS currency_id,
                detail.uom_quantity AS uom_quantity,
                detail.price_unit AS price_unit,
                detail.price_subtotal AS price_subtotal,
                detail.price_tax AS price_tax,
                detail.price_total AS price_total
            FROM school_enrollment_payment_term_extra_detail detail
            JOIN school_enrollment_payment_term term ON term.id = detail.term_id
            JOIN school_extracurricular_participant participant
                ON participant.id = detail.participant_id
            JOIN school_extracurricular_offering offering
                ON offering.id = participant.offering_id
            LEFT JOIN school sch ON sch.id = participant.school_id

            UNION ALL

            SELECT
                (detail.id * 2 + 1) AS id,
                'standalone' AS billing_route,
                term.participant_id AS participant_id,
                participant.offering_id AS offering_id,
                offering.extracurricular_id AS extracurricular_id,
                offering.category_id AS category_id,
                participant.student_id AS student_id,
                participant.partner_id AS partner_id,
                participant.school_id AS school_id,
                sch.company_id AS company_id,
                participant.academic_year_id AS academic_year_id,
                participant.academic_term_id AS academic_term_id,
                offering.teacher_id AS teacher_id,
                detail.product_id AS product_id,
                detail.product_category_id AS product_category_id,
                term.customer_invoice_id AS customer_invoice_id,
                detail.currency_id AS currency_id,
                detail.uom_quantity AS uom_quantity,
                detail.price_unit AS price_unit,
                detail.price_subtotal AS price_subtotal,
                detail.price_tax AS price_tax,
                detail.price_total AS price_total
            FROM school_extracurricular_payment_term_detail detail
            JOIN school_extracurricular_payment_term term ON term.id = detail.term_id
            JOIN school_extracurricular_participant participant
                ON participant.id = term.participant_id
            JOIN school_extracurricular_offering offering
                ON offering.id = participant.offering_id
            LEFT JOIN school sch ON sch.id = participant.school_id
        """
