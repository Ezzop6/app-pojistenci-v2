from termcolor import colored
from .password_generator import PasswordGenerator

def cprint(text, color="light_green"):
    print(colored(text, color))
    
def random_secret_key():
    randon_secret_string = PasswordGenerator(10,10,10).generate_password()
    return randon_secret_string

