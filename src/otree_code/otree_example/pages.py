# Code heavily inspired by MPL implementation of Felix Holzmeister: https://github.com/felixholzmeister/mpl
# Holzmeister, F. (2017). oTree: Ready-Made Apps for Risk Preference Elicitation Methods, Journal of Behavioral and Experimental Finance 16, 33-38.

from otree.api import Currency as c
from otree.api import currency_range

from ._builtin import Page
from ._builtin import WaitPage
from .models import Constants


class Intro(Page):
    pass


class MPL(Page):
    form_model = "player"

    def get_form_fields(self):
        return Constants.decisions

    def vars_for_template(self):
        return dict(
            payoff_charity=Constants.payoff_charity,
            choices=list(zip(Constants.self_payments, Constants.decisions)),
        )

    def before_next_page(self):
        # update mpl_decisions_made
        form_fields = self.participant.vars["mpl_decisions"]
        for j, decision in zip(range(0, len(Constants.self_payments)), form_fields):
            decision_i = getattr(self.player, decision)
            self.participant.vars["mpl_decisions_made"][j] = decision_i

        # notarization:
        if Constants.blockchain_notarization == True:
            self.player.notarize_player_input()


class Results(Page):
    pass


page_sequence = [Intro, MPL, Results]
