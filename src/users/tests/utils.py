import random
import string


def generate_random_password():
    N = random.randint(7, 30)
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=N))