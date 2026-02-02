import string
from .models import ShortURL

BASE62_ALPHABET = string.digits + string.ascii_letters

def base62_encode(num):
    if num == 0:
        return BASE62_ALPHABET[0]
    chars = []
    base = len(BASE62_ALPHABET)
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(chars))

def generate_short_key(length=6):
    last = ShortURL.objects.order_by('-id').first()
    next_id = 1 if not last else last.id + 1
    key = base62_encode(next_id)
    return key.rjust(length, '0')
