from io import BytesIO

from flask import Flask, request, send_file
from flask_api.status import HTTP_400_BAD_REQUEST

from zmanim.res.image.picture_maker import get_picture


app = Flask(__name__)

picture_types = ['zmanim', 'shabbos', 'rosh_chodesh', 'daf_yomi', 'rosh_hashana',
                 'yom_kippur', 'succos', 'shmini_atseres', 'chanukah', 'purim', 'pesach',
                 'shavuos', 'tu_bishvat', 'lag_baomer', 'israel_holidays', 'fast']


def validate_request_data():
    if not request.is_json:
        return 'JSON format is required!', HTTP_400_BAD_REQUEST

    json_data = request.get_json()
    # todo add api key

    if 'lang' not in json_data:
        return 'Param `lang` is required!', HTTP_400_BAD_REQUEST
    if 'picture_type' not in json_data:
        return 'Param `picture_type` is required!', HTTP_400_BAD_REQUEST
    if 'payload' not in json_data:
        return 'Param `payload` is required!', HTTP_400_BAD_REQUEST
    if json_data['picture_type'] not in picture_types:
        return f'Wrong picture type `{json_data["picture_type"]}`', HTTP_400_BAD_REQUEST


def process_data() -> BytesIO:
    json_data = request.get_json()
    picture_class = get_picture(json_data['picture_type'])
    picture = picture_class(lang=json_data['lang'], data=json_data['payload']
                            ).draw_picture()
    return picture


@app.route('/', methods=['GET'])
def index():
    errors = validate_request_data()
    if errors:
        return errors
    picture = process_data()

    return send_file(picture, mimetype='image/jpeg')


app.run()
