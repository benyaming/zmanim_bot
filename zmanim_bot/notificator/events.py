from __future__ import annotations

from datetime import datetime as dt

from .trigger import EventTrigger


class Event(dt):
    owner_id: int
    name: str
    message: str
    dt: dt
    trigger: EventTrigger




