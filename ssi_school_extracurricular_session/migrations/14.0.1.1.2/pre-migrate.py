# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.1 -> 14.0.1.1.2
#
# Changes: session_participant_uniq is no longer a database-level
#          ``_sql_constraints`` entry -- it is now enforced by
#          ``@api.constrains`` so violations raise a readable
#          ValidationError instead of a raw psycopg2.IntegrityError.
#          Changing the Python code alone does not drop the physical
#          constraint on an already-installed database, so it is
#          dropped here.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Drop the obsolete ``session_participant_uniq`` SQL constraint.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; alters
        ``school_extracurricular_session_attendance``
    """
    openupgrade.delete_sql_constraint_safely(
        env,
        "ssi_school_extracurricular_session",
        "school_extracurricular_session_attendance",
        "session_participant_uniq",
    )
    _logger.info(
        "Dropped physical constraint session_participant_uniq on "
        "school_extracurricular_session_attendance."
    )
