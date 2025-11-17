import string
import random


def get_unique_short_id():
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(6))
        return short_id
