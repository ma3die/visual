from uuid import uuid4
from pytils.translit import slugify
import magic

def get_mime_type(file):
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    file_type = mime_type.split('/')[0]
    return file_type


def unique_slugify(instance, slug):
    """Генератор уникальных SLUG для моделей"""
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug
