from datetime import datetime as dt
from typing import List, Optional, Tuple

from odmantic import EmbeddedModel, Field, Model

from zmanim_bot.config import config
from zmanim_bot.exceptions import NoLocationException, UnknownProcessorException
from zmanim_bot.processors import PROCESSORS
from zmanim_bot.processors.base import BaseProcessor

HAVDALA_OPINIONS = ['tzeis_5_95_degrees', 'tzeis_8_5_degrees', 'tzeis_42_minutes', 'tzeis_72_minutes']


class UserInfo(EmbeddedModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class UserMeta(EmbeddedModel):
    last_seen_at: dt = Field(default_factory=dt.now)
    is_banned_by_admin: bool = False
    is_user_blocked_bot: bool = False


class Location(EmbeddedModel):
    lat: float
    lng: float
    name: str
    is_active: bool
    elevation: int | None = 0

    @property
    def coordinates(self) -> Tuple[float, float, int]:
        elevation = self.elevation if self.elevation >= 0 else 0
        return self.lat, self.lng, elevation


class OmerSettings(EmbeddedModel):
    is_enabled: bool = False
    is_sent_today: Optional[bool]
    notification_time: Optional[str]


class ZmanimSettings(EmbeddedModel):
    alos: bool = True
    misheyakir_10_2: bool = True
    sunrise: bool = True
    sof_zman_shema_ma: bool = False
    sof_zman_shema_gra: bool = True
    sof_zman_tefila_ma: bool = False
    sof_zman_tefila_gra: bool = True
    chatzos: bool = True
    mincha_gedola: bool = True
    mincha_ketana: bool = False
    plag_mincha: bool = False
    sunset: bool = True
    tzeis_5_95_degrees: bool = False
    tzeis_8_5_degrees: bool = True
    tzeis_42_minutes: bool = False
    tzeis_72_minutes: bool = False
    chatzot_laila: bool = False
    astronomical_hour_ma: bool = False
    astronomical_hour_gra: bool = False


class User(Model):
    user_id: int
    personal_info: UserInfo = Field(default_factory=UserInfo)

    language: Optional[str] = None
    location_list: List[Location] = Field(default_factory=list)
    cl_offset: int = 18
    havdala_opinion: str = 'tzeis_8_5_degrees'
    zmanim_settings: ZmanimSettings = Field(default_factory=ZmanimSettings)
    processor_type: str = 'image'
    omer: OmerSettings = Field(default_factory=OmerSettings)
    # The calendar site's full settings snapshot (serialized JSON), stored
    # verbatim for cross-device sync — opaque to the bot (see the miniapp API).
    web_prefs: Optional[str] = None

    meta: UserMeta = Field(default_factory=UserMeta)

    class Config:
        collection = config.DB_COLLECTION_NAME
        parse_doc_with_default_factories = True

    @property
    def location(self) -> Location:
        loc = list(filter(lambda l: l.is_active, self.location_list))
        if not loc:
            raise NoLocationException
        return loc[0]

    def get_location_by_coords(self, lat: float, lng: float) -> Location:
        resp = list(filter(lambda loc: loc.lat == lat and loc.lng == lng, self.location_list))
        if not resp:
            raise NoLocationException
        return resp[0]

    def get_processor(self, location: Optional[Location] = None) -> BaseProcessor:
        try:
            return PROCESSORS[self.processor_type]((location and location.name) or self.location.name)
        except KeyError:
            raise UnknownProcessorException()



class WebSync(Model):
    """A calendar-site settings blob for someone with no Telegram account.

    Deliberately NOT a `User`: user documents are Telegram-shaped (`user_id` is
    a Telegram id, `personal_info` comes from Telegram) and `broadcast` iterates
    that collection to message everyone — synthetic rows there would corrupt
    both. This is a plain key-value row instead, in its own collection.

    The credential is `key` plus its signature (see api.websync_signature):
    both come from /google-key after a Google ID token is verified, so only a
    real signed-in account can read or create a row — the bot need not keep any
    session. `account` is a one-way hash of the Google `sub` (never the id
    itself); /google-key looks a row up by it and mints `key` once, so the key
    is **stable across bot-token rotations** — a rotation invalidates the
    token-derived `sig` and forces a re-sign-in, but the same key (hence the
    same data) is handed back. The bot never interprets `blob`; it only bounds
    its size and checks it is JSON, as for `User.web_prefs`. `updated_at`
    carries a TTL index (see utils.ensure_mongo_index) so a blob no device has
    touched in a long time is reaped; an active device keeps refreshing it.

    Indexes (both created in utils.ensure_mongo_index): `account` is unique but
    **sparse** — pre-account rows have no such field and several nulls would
    otherwise collide on a plain unique index.
    """

    account: Optional[str] = None
    key: str = Field(index=True, unique=True)
    blob: str
    updated_at: dt = Field(default_factory=dt.utcnow)

    class Config:
        collection = 'web_sync'
        parse_doc_with_default_factories = True


class WebPrefs(Model):
    """A Telegram user's calendar-site settings blob, stored APART from their
    `User` document.

    It used to live on `User.web_prefs`, but the bot mutates `User` through
    full-document saves in a dozen setters (language, location, …). A website
    blob sync and any such save racing on the same user would let the save's
    stale copy revert the blob (see the miniapp API). Keeping it in its own
    collection, keyed by `user_id` and written only by the website, takes it
    out of every `User` save entirely. `User.web_prefs` remains only as a
    read-fallback for rows written before this split; the website's next sync
    populates the row here and it becomes authoritative.
    """

    user_id: int = Field(index=True, unique=True)
    blob: str
    updated_at: dt = Field(default_factory=dt.utcnow)

    class Config:
        collection = 'web_prefs'
        parse_doc_with_default_factories = True
