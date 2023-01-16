from odmantic import Model

from zmanim_bot.notificator.trigger import EventTrigger


class Event(Model):
    owner_id: int
    name: str
    message: str
    trigger: EventTrigger
