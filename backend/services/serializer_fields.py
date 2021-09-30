from django.core.files.base import ContentFile
from django.db import models

from rest_framework import serializers

import time
import base64
import webcolors
from typing import Union


class Base64ToContentFileField(serializers.Field):
    def to_representation(self, image: models.ImageField) -> Union[str, None]:
        return image.url if image else None

    def to_internal_value(self, data: str) -> ContentFile:
        """Accepts a base64-encoded string and returns django
        ContentFile instance.
        """
        try:
            _, base64_string = data.split(';base64,')
            return ContentFile(
                content=base64.b64decode(base64_string),
                name=f'{time.time()}.webp'
            )
        except Exception as e:
            raise serializers.ValidationError(
                'Failed to convert base64-string to a ContentFile instance.'
            )


class HEXToColourNameField(serializers.Field):
    def to_representation(self, color_name: str) -> str:
        try:
            return webcolors.name_to_hex(color_name)
        except Exception as e:
            raise serializers.ValidationError(
                ('Failed to convert human-readable color name'
                 'to hex representation.')
            )

    def to_internal_value(self, hex_color: str) -> str:
        """Accepts a color name as hexadecimal representation and returns
        human-readable text.
        """
        try:
            return webcolors.hex_to_name(hex_color)
        except Exception as e:
            raise serializers.ValidationError(
                'There is no such color name for the given hex.'
            )
