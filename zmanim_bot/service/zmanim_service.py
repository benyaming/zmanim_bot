from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.integrations import zmanim_api_client
from zmanim_bot.integrations.zmanim_models import Zmanim
from zmanim_bot.repository import bot_repository
from zmanim_bot.states import ZmanimGregorianDateState


async def get_zmanim() -> Zmanim:
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_zmanim(
        user.location.coordinates,
        user.zmanim_settings.dict()
    )
    return data


async def send_zmanim(*, date: str = None, call_data: str = None):
    if call_data:
        date = call_data.split(CallbackPrefixes.zmanim_by_date)[1]

    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_zmanim(
        user.location.coordinates,
        user.zmanim_settings.dict(),
        date_=date
    )
    await user.processor.send_zmanim(data)


async def init_zmanim_by_date():
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()


async def get_shabbat():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_shabbat(
        location=user.location.coordinates,
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )
    await user.processor.send_shabbat(data)


async def get_daf_yomi():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_daf_yomi()
    await user.processor.send_daf_yomi(data)


async def get_rosh_chodesh():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_rosh_chodesh()
    await user.processor.send_rosh_chodesh(data)
