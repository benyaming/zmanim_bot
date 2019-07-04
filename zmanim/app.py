from aiohttp import web

from zmanim.res.image.picture_maker import PictureFactory
from zmanim.res.image.picture_types import PictureTypes

data = {
    'day': 1,
    'month': 9,
    'year': 2222,
    'dow': 1
}


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.tu_bishvat, 'Russian', data)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)

# python c:\Users\Benyomin\AppData\Local\Programs\Python\Python37-32\Tools\i18n\pygettext.py -d jcb_img_processor zmanim\res\localizations\utils.py
