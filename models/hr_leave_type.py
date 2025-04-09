
from odoo import fields, models


class HrLeaveType(models.Model):
    """This module inherits from the 'hr.leave.type' model of the Odoo Time Off
    Module. It adds a new field called 'leave_code', which is a selection field
    that allows users to choose from a list of predefined leave codes."""
    _inherit = 'hr.leave.type'

    leave_code = fields.Selection(
        [('UL', 'UL'),
         ('SL', 'SL'),
         ('RL', 'RL'),
         ('NL', 'NL'),
         ('ML', 'ML'),
         ('FL', 'FL'),
         ('CL', 'CL'),
         ('PL', 'PL'),
         ('OL', 'OL'),
         ('WFH','WFH')],
        required=True,
        string="Leave Code",
        default="NL",
        help="UL = Unpaid Leave\n"
             " SL = Sick Leave\n"
             " RL = Regular Leave\n"
             " NL = Normal Leave\n"
             " ML = Maternity Leave\n"
             " FL = Festival Leave\n"
             " CL = Compensatory Leave\n"
             " PL = Paid Leave\n"
             " OL = Other Leave\n"
             " WFH = WFH\n")
