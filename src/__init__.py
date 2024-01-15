from .args_parser import Args, ColoredArgumentParser
import string, random

def random_name():
    arg = list(string.ascii_lowercase) + list(string.digits)
    random.shuffle(arg)
    return ''.join(
        random.choice(arg) for _ in range(random.randint(8, 16))
    ).lower()