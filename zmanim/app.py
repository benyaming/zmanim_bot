from aiohttp import web

from zmanim.res.image.picture_maker import PictureFactory
from zmanim.res.image.picture_types import PictureTypes

data = {
        'year': 2019,
        'part_1': {
            'day_1': {
                'eve_day': 5,
                'eve_month': 9,
                'day': 6,
                'month': 9,
                'dow': 0,
                'cl': 'cl_11',
                'havdala': 'ha_11'
            },
            'day_2': None,
            #     'day': 7,
            #     'month': 9,
            #     'dow': int
            #     'cl': str,
            #     'havdala': Optional[str]
            # }],
            'day_3': None
            #     'day': 8,
            #     'month': 9,
            #     'dow': int
            #     'cl': str,
            #     'havdala': Optional[str]
            # },
        },
        'part_2': {
            'day_1': {
                'eve_day': 5,
                'eve_month': 9,
                'day': 6,
                'month': 9,
                'dow': 0,
                'cl': 'cl_11',
                'havdala': 'ha_11'
            },
            'day_2': None,
            #     'day': 7,
            #     'month': 9,
            #     'dow': int
            #     'cl': str,
            #     'havdala': Optional[str]
            # }],
            'day_3': None
            #     'day': 8,
            #     'month': 9,
            #     'dow': int
            #     'cl': str,
            #     'havdala': Optional[str]
            # },
        },
    }


async def handle(request: web.Request):
    response = PictureFactory.get_picture(PictureTypes.pesach, 'Russian', data)
    return web.Response(body=response, content_type='image/jpeg')


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=2000)

# python c:\Users\Benyomin\AppData\Local\Programs\Python\Python37-32\Tools\i18n\pygettext.py -d jcb_img_processor zmanim\res\localizations\utils.py
