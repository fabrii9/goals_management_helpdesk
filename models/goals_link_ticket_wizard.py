# -*- coding: utf-8 -*-
from odoo import fields, models


class GoalsLinkTicketWizard(models.TransientModel):
    """Wizard para vincular tickets de helpdesk ya existentes a un objetivo semanal."""

    _name = 'goals.link.ticket.wizard'
    _description = 'Vincular tickets a objetivo'

    goal_id = fields.Many2one(
        comodel_name='goals.goal',
        string='Objetivo semanal',
        required=True,
        domain="[('period_type', '=', 'week')]",
        default=lambda self: self.env.context.get('default_goal_id'),
    )
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='goals_link_ticket_wizard_ticket_rel',
        column1='wizard_id',
        column2='ticket_id',
        string='Tickets',
        help='Tickets que se asociarán al objetivo semanal seleccionado.',
    )

    def action_link(self):
        """Asocia los tickets seleccionados al objetivo semanal."""
        for wizard in self:
            if wizard.goal_id and wizard.ticket_ids:
                wizard.ticket_ids.write({'objective_id': wizard.goal_id.id})
        return {'type': 'ir.actions.act_window_close'}
