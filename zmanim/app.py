import json

from aiohttp import web

from zmanim.res.picture_maker import PictureFactory
from zmanim.res.picture_types import PictureTypes

text = 'Дата: |23-30 декабря 2018,^Понедельник-Понедельник'


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.chanukah, '', text)
    print(response)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)
