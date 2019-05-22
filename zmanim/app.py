from aiohttp import web

from zmanim.res.image.picture_maker import PictureFactory
from zmanim.res.image.picture_types import PictureTypes

data = {
    'parasha': 'Bo',
    'candle_lighting': '11:11',
    'shkia_offset': 18,
    'tzeit_kochavim': '22:22',
    'error': False,
    'warning': True
}


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.shabbos, 'Russian', data)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)
