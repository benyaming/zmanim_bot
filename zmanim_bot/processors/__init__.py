from zmanim_bot.processors.base import BaseProcessor

from .image.image_processor import ImageProcessor
from .text.text_processor import TextProcessor

PROCESSORS = {
    'image': ImageProcessor,
    'text': TextProcessor
}
