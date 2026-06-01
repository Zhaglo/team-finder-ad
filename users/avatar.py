import random
import uuid
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import (
    AVATAR_BACKGROUND_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
)


def get_first_letter(name):
    if not name:
        return '?'

    return name[0].upper()


def get_default_font():
    try:
        return ImageFont.load_default(size=AVATAR_FONT_SIZE)
    except TypeError:
        return ImageFont.load_default()


def get_font():
    font_path = (
        settings.BASE_DIR
        / 'static'
        / 'fonts'
        / 'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf'
    )

    try:
        return ImageFont.truetype(str(font_path), AVATAR_FONT_SIZE)
    except OSError:
        return get_default_font()


def generate_avatar_image(name):
    first_letter = get_first_letter(name)
    background_color = random.choice(AVATAR_BACKGROUND_COLORS)

    image = Image.new(
        'RGB',
        (AVATAR_SIZE, AVATAR_SIZE),
        background_color,
    )
    draw = ImageDraw.Draw(image)
    font = get_font()

    text_bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (AVATAR_SIZE - text_width) / 2
    y = (AVATAR_SIZE - text_height) / 2 - 10

    draw.text(
        (x, y),
        first_letter,
        fill=AVATAR_TEXT_COLOR,
        font=font,
    )

    buffer = BytesIO()
    image.save(buffer, format='PNG')

    return ContentFile(buffer.getvalue())


def generate_avatar_filename():
    return f'{uuid.uuid4()}.png'


def generate_user_avatar(name):
    return generate_avatar_filename(), generate_avatar_image(name)
