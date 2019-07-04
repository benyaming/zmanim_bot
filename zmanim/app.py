from aiohttp import web

from zmanim.res.image.picture_maker import PictureFactory
from zmanim.res.image.picture_types import PictureTypes

data = {
    'year': 2019,
    'day_1': {
        'eve_day': 1,
        'eve_month': 9,
        'day': 2,
        'month': 9,
        'dow': 4,
        'cl': 'xx:xx',
        'havdala': 'qq:qq'
    },
    'day_2': {
        'day': 3,
        'month': 9,
        'dow': 5,
        'cl': 'yy:yy',
        'havdala': 'zz:zz'
    },
    'day_3': {
        'day': 4,
        'month': 9,
        'dow': 6,
        'cl': 'clsh',
        'havdala': 'hash'
    },
    'hoshana_raba': {
        'day': 6,
        'month': 9,
        'dow': 1
    },
}


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.succos, 'Russian', data)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)

# python c:\Users\Benyomin\AppData\Local\Programs\Python\Python37-32\Tools\i18n\pygettext.py -d jcb_img_processor zmanim\res\localizations\utils.py
