# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolExtracurricularSession(models.Model):
    """Builds instructor honor documents when a session is done.

    Every ``instructor_ids`` line recorded ``present`` and identified
    by a ``partner_id`` (an external coach/assistant, not a school
    ``teacher_id``) gets one ``outsource_work`` document, following
    the preset established by
    ``ssi_psychology_consultation_outsource_work``: build a ``new()``
    record, run the same onchange chain the form would run, then
    ``create()`` from the resolved values. Internal instructors are
    skipped -- their honor is payroll, not accounts payable.
    """

    _name = "school_extracurricular_session"
    _inherit = [
        "school_extracurricular_session",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
    _work_log_page_xpath = "//page[@name='description']"
    _work_log_template_position = "after"

    def _prepare_session_instructor_data(self, template_line):
        """Carry the outsource work fields onto the copied roster line.

        Extends the base extension point so a session generated (or
        edited before instructors are filled) from an Offering keeps
        the template line's outsource work configuration -- without
        this override, every session-side roster line would start
        blank and every Done would fail the Outsource Work Type/Usage
        checks even when the Offering template has them set.

        :param template_line: the
            ``school_extracurricular_offering_instructor`` template
            line being copied
        :return: dict of ``school_extracurricular_session_instructor``
            values, without ``session_id``
        """
        values = super()._prepare_session_instructor_data(template_line)
        values["outsource_work_type_id"] = template_line.outsource_work_type_id.id
        values["outsource_work_usage_id"] = template_line.outsource_work_usage_id.id
        return values

    def _done(self):
        """Mark this session done, then build instructor honor logs.

        Side effect: creates one ``outsource_work`` per present,
        externally-identified instructor roster line that does not
        already have one.

        :raises UserError: propagated from
            ``_create_instructor_outsource_work`` when a roster line
            or its offering is missing required outsource work
            configuration
        """
        super()._done()
        for record in self:
            record._create_instructor_outsource_work()

    def _create_instructor_outsource_work(self):
        """Create the missing honor documents of this session.

        Idempotent: a roster line whose ``partner_id`` already has a
        non-cancelled ``outsource_work`` on this session is skipped,
        so restarting and marking a session done again does not
        duplicate honor documents.

        :return: None
        """
        self.ensure_one()
        existing_partners = self.outsource_work_ids.filtered(
            lambda work: work.state != "cancel"
        ).mapped("partner_id")
        candidates = self.instructor_ids.filtered(
            lambda line: (
                line.attendance_state == "present"
                and line.partner_id
                and line.partner_id not in existing_partners
            )
        )
        for line in candidates:
            self._create_outsource_work(line)

    def _create_outsource_work(self, line):
        """Build and create one honor document for one roster line.

        :param line: the ``school_extracurricular_session_instructor``
            line the honor document is built for
        :raises UserError: when a prerequisite is missing (see
            ``_check_outsource_work_prerequisite``)
        :return: None
        """
        self.ensure_one()
        pricelist = self._check_outsource_work_prerequisite(line)
        OutsourceWork = self.env["outsource_work"]
        ctx = {"outsource_work_model": self._name}
        temp_record = OutsourceWork.with_context(ctx).new(
            self._prepare_outsource_work_data(line, pricelist)
        )
        temp_record = self._compute_outsource_work_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        OutsourceWork.create(values)

    def _check_outsource_work_prerequisite(self, line):
        """Validate that one roster line may get an honor document.

        :param line: the ``school_extracurricular_session_instructor``
            line being checked
        :raises UserError: when the offering has no Analytic Account,
            when the line has no Outsource Work Type, when the line
            has no Outsource Work Usage, or when no open Outsource
            Work Rate covers this person on this session's date
        :return: the resolved ``product.pricelist`` for this line
        :rtype: recordset
        """
        self.ensure_one()
        if not self.offering_id.analytic_account_id:
            error_message = (
                _(
                    """
Context: Create instructor outsource work
Database ID: %s
Problem: Offering '%s' has no Analytic Account
Solution: Set an Analytic Account on the Offering before marking the
session as done
"""
                )
                % (self.id, self.offering_id.display_name)
            )
            raise UserError(error_message)
        if not line.outsource_work_type_id:
            error_message = (
                _(
                    """
Context: Create instructor outsource work
Database ID: %s
Problem: Instructor roster line for '%s' has no Outsource Work Type
Solution: Set an Outsource Work Type on the roster line before
marking the session as done
"""
                )
                % (self.id, line.partner_id.display_name)
            )
            raise UserError(error_message)
        if not line.outsource_work_usage_id:
            error_message = (
                _(
                    """
Context: Create instructor outsource work
Database ID: %s
Problem: Instructor roster line for '%s' has no Outsource Work Usage
Solution: Set an Outsource Work Usage on the roster line before
marking the session as done
"""
                )
                % (self.id, line.partner_id.display_name)
            )
            raise UserError(error_message)
        pricelist = self._get_outsource_work_pricelist(line)
        if not pricelist:
            error_message = (
                _(
                    """
Context: Create instructor outsource work
Database ID: %s
Problem: No open Outsource Work Rate covers '%s' on '%s'
Solution: Create an open Outsource Work Rate for this person that
covers the session date
"""
                )
                % (self.id, line.partner_id.display_name, self.date)
            )
            raise UserError(error_message)
        return pricelist

    def _prepare_outsource_work_data(self, line, pricelist):
        """Build the create values of one honor document.

        :param line: the ``school_extracurricular_session_instructor``
            line the honor document is built for
        :param pricelist: the ``product.pricelist`` resolved by
            ``_get_outsource_work_pricelist``
        :return: dict of ``outsource_work`` values, without the
            fields the onchange chain still has to fill
        :rtype: dict
        """
        self.ensure_one()
        return {
            "model_id": self._get_outsource_work_model_id(),
            "work_object_id": self.id,
            "date": self.date,
            "partner_id": line.partner_id.id,
            "type_id": line.outsource_work_type_id.id,
            "product_id": line.outsource_work_type_id.product_id.id,
            "usage_id": line.outsource_work_usage_id.id,
            "analytic_account_id": self.offering_id.analytic_account_id.id,
            "pricelist_id": pricelist.id,
            "uom_quantity": 1.0,
        }

    def _get_outsource_work_model_id(self):
        """Resolve the ``ir.model`` of this session's model.

        :return: id of the ``ir.model`` record for
            ``school_extracurricular_session``
        :rtype: int
        """
        self.ensure_one()
        Model = self.env["ir.model"]
        criteria = [("model", "=", self._name)]
        return Model.search(criteria, limit=1).id

    def _compute_outsource_work_onchange(self, temp_record):
        """Run the onchange chain a manually-filled form would run.

        ``mixin.product_line_account.account_id`` is required and is
        only ever filled through ``onchange_account_id``, which in
        turn needs ``usage_id`` -- already set in
        ``_prepare_outsource_work_data`` -- to resolve it.

        ``onchange_pricelist_id`` is deliberately NOT called here: it
        unconditionally clears ``pricelist_id`` and only refills it
        from ``allowed_pricelist_ids[0]``, which this model's
        configurator never populates. Calling it would discard the
        pricelist ``_prepare_outsource_work_data`` already resolved
        from the matching ``outsource_work_rate``.

        :param temp_record: an ``outsource_work`` record built with
            ``new()``
        :return: the same record, with the onchange-derived fields
            filled in
        :rtype: recordset
        """
        temp_record.onchange_account_id()
        temp_record.onchange_uom_id()
        temp_record.onchange_price_unit()
        return temp_record

    def _get_outsource_work_pricelist(self, line):
        """Resolve the pricelist to honor one roster line with.

        Searches ``outsource_work_rate`` for the most recent ``open``
        rate covering this person on this session's date, then reads
        the pricelist off the detail line matching the roster line's
        product.

        :param line: the ``school_extracurricular_session_instructor``
            line being priced
        :return: the resolved ``product.pricelist``, or an empty
            recordset when no rate/detail matches
        :rtype: recordset
        """
        self.ensure_one()
        Rate = self.env["outsource_work_rate"]
        criteria = [
            ("partner_id", "=", line.partner_id.id),
            ("state", "=", "open"),
            ("date_start", "<=", self.date),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", self.date),
        ]
        rates = Rate.search(criteria, order="date_start desc")
        product = line.outsource_work_type_id.product_id
        for rate in rates:
            detail = rate.detail_ids.filtered(
                lambda line_detail: line_detail.product_id == product
            )
            if detail:
                return detail[0].pricelist_id
        return self.env["product.pricelist"]

    def _cancel(self, cancel_reason):
        """Cancel this session, then delete its non-cancelled honors.

        :param cancel_reason: the reason text supplied by the wizard
        :raises UserError: when a non-cancelled honor document
            already has an Outstanding -- nothing is cancelled or
            deleted in that case
        :return: None
        """
        self.ensure_one()
        self._check_outsource_work_deletable()
        super()._cancel(cancel_reason)
        self._delete_outsource_work()

    def _restart(self):
        """Restart this session, then delete its non-cancelled honors.

        Deleting them lets ``_done`` rebuild a clean set of honor
        documents the next time this session is marked done, instead
        of finding stale lines already occupying every present
        instructor's ``partner_id``.

        :raises UserError: when a non-cancelled honor document
            already has an Outstanding -- nothing is restarted or
            deleted in that case
        :return: None
        """
        self.ensure_one()
        self._check_outsource_work_deletable()
        super()._restart()
        self._delete_outsource_work()

    def _check_outsource_work_deletable(self):
        """Validate that this session's honors may be discarded.

        :raises UserError: when a non-cancelled ``outsource_work`` on
            this session already has an Outstanding
        :return: None
        """
        self.ensure_one()
        blocking = self.outsource_work_ids.filtered(
            lambda work: work.state != "cancel" and work.outstanding_id
        )
        if blocking:
            error_message = (
                _(
                    """
Context: Cancel or restart extracurricular session
Database ID: %s
Problem: An instructor outsource work log already has an Outstanding
Solution: Cancel the Outsource Work Outstanding before cancelling or
restarting this session
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

    def _delete_outsource_work(self):
        """Delete this session's non-cancelled honor documents.

        :return: None
        """
        self.ensure_one()
        works = self.outsource_work_ids.filtered(lambda work: work.state != "cancel")
        works.unlink()
