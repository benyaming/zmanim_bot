from zmanim_bot.processors.base import BaseProcessor

from .image.image_processor import ImageProcessor

PROCESSORS = {
    'image': ImageProcessor
}
