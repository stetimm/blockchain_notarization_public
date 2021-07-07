# Don't change anything in this file.
import otree.api

from .. import models


class Page(otree.api.Page):
    subsession: models.Subsession
    group: models.Group
    player: models.Player


class WaitPage(otree.api.WaitPage):
    subsession: models.Subsession
    group: models.Group
    player: models.Player


class Bot(otree.api.Bot):
    subsession: models.Subsession
    group: models.Group
    player: models.Player
