import time
import base64
import webcolors
from typing import Union
from django.core.files.base import ContentFile
from django.db import models
from rest_framework import serializers


class Base64ToContentFileField(serializers.Field):
    def to_representation(self, image: models.ImageField) -> Union[str, None]:
        return image.url if image else None

    def to_internal_value(self, data: str) -> ContentFile:
        """Accepts base64-encoded string and returns django
        ContentFile instance.
        """
        try:
            _, base64_string = data.split(';base64,')
            return ContentFile(
                content=base64.b64decode(base64_string),
                name=f'{time.time()}.webp'
            )
        except Exception:
            raise serializers.ValidationError(
                'Failed to convert base64-string to ContentFile instance.'
            )


class HEXToColourNameField(serializers.Field):
    def to_representation(self, colour_name: str) -> str:
        return colour_name

    def to_internal_value(self, hex_colour: str) -> str:
        """Accepts a colour name as hexadecimal representation and returns
        human-readable text.
        """
        try:
            return webcolors.hex_to_name(hex_colour)
        except Exception:
            raise serializers.ValidationError(
                'There is no such colour name.'
            )
