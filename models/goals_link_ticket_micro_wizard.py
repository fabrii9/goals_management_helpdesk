# -*- coding: utf-8 -*-
from odoo import fields, models


class GoalsLinkTicketMicroWizard(models.TransientModel):
    """Wizard para vincular tickets de helpdesk ya existentes a un microobjetivo."""

    _name = 'goals.link.ticket.micro.wizard'
    _description = 'Vincular tickets a microobjetivo'

    micro_objective_id = fields.Many2one(
        comodel_name='goals.micro.objective',
        string='Microobjetivo',
        required=True,
        default=lambda self: self.env.context.get('default_micro_objective_id'),
    )
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='goals_link_ticket_micro_wizard_ticket_rel',
        column1='wizard_id',
        column2='ticket_id',
        string='Tickets',
        help='Tickets que se asociarán al microobjetivo seleccionado.',
    )

    def action_link(self):
        """Asocia los tickets seleccionados al microobjetivo."""
        for wizard in self:
            if wizard.micro_objective_id and wizard.ticket_ids:
                wizard.ticket_ids.write({
                    'micro_objective_id': wizard.micro_objective_id.id,
                    'objective_id': False,
                })
        return {'type': 'ir.actions.act_window_close'}
