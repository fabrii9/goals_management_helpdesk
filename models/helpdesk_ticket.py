# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpdeskTicket(models.Model):
    """Extensión de tickets de helpdesk para vincularlos a microobjetivos."""

    _inherit = 'helpdesk.ticket'

    micro_objective_id = fields.Many2one(
        comodel_name='goals.micro.objective',
        string='Microobjetivo',
        index=True,
        help='Microobjetivo al que contribuye este ticket.',
    )
    goal_id = fields.Many2one(
        comodel_name='goals.goal',
        string='Objetivo semanal',
        related='micro_objective_id.goal_id',
        store=True,
        index=True,
    )

    def write(self, vals):
        was_closed = {ticket.id: ticket.stage_id.fold for ticket in self}
        result = super(HelpdeskTicket, self).write(vals)
        for ticket in self:
            if ticket.stage_id.fold and not was_closed.get(ticket.id):
                ticket._goals_notify_ticket_completed()
        return result

    def _goals_notify_ticket_completed(self):
        """Hook invocado cuando un ticket pasa a etapa cerrada."""
        self.ensure_one()
        if not self.micro_objective_id:
            return
        if self.env['ir.config_parameter'].sudo().get_param(
            'goals_management.gamification_enabled'
        ):
            xp = int(self.env['ir.config_parameter'].sudo().get_param(
                'goals_management.xp_task', default=10
            ))
            if self.user_id:
                self.user_id.goals_grant_xp(
                    xp,
                    source='ticket_completed',
                    source_model='helpdesk.ticket',
                    source_res_id=self.id,
                    description=f"Ticket completado: {self.name}",
                )
        self._goals_try_complete_micro_objective()

    def _goals_try_complete_micro_objective(self):
        """Marca el microobjetivo como done si todas sus tareas/tickets están cerrados."""
        self.ensure_one()
        micro = self.micro_objective_id
        if not micro or micro.state in {'done', 'cancelled'}:
            return
        tasks = micro.task_ids.filtered(lambda t: t.active)
        tickets = micro.ticket_ids
        all_tasks_closed = all(task.is_closed for task in tasks) if tasks else True
        all_tickets_closed = all(ticket.stage_id.fold for ticket in tickets) if tickets else True
        if tasks or tickets:
            if all_tasks_closed and all_tickets_closed:
                micro.action_done()


class GoalsMicroObjective(models.Model):
    """Extensión de microobjetivos para incluir tickets de helpdesk en el progreso."""

    _inherit = 'goals.micro.objective'

    ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='micro_objective_id',
        string='Tickets',
    )

    def _get_progress_contributions(self):
        """Suma los tickets cerrados al cálculo de progreso."""
        self.ensure_one()
        completed, total = super(GoalsMicroObjective, self)._get_progress_contributions()
        tickets = self.ticket_ids
        completed += sum(1 for ticket in tickets if ticket.stage_id.fold)
        total += len(tickets)
        return completed, total
