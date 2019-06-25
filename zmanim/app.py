from aiohttp import web

from zmanim.res.image.picture_maker import PictureFactory
from zmanim.res.image.picture_types import PictureTypes

data = {
    'date': {
        'year': 2019,
        'months': [9],
        'days': [4, 5],
        'dows': [1, 2]
    },
    'candle_lighting': '11:11',
    'havdala': '22:22'
}


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.yom_kippur, 'Russian', data)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)

# python c:\Users\Benyomin\AppData\Local\Programs\Python\Python37-32\Tools\i18n\pygettext.py -d jcb_img_processor zmanim\res\localizations\utils.py
