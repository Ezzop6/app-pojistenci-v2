from termcolor import colored
from .password_generator import PasswordGenerator
from os import listdir
from random import choice

def cprint(text, color="light_green"):
    print(colored(text, color))
    
def random_secret_key():
    randon_secret_string = PasswordGenerator(10,10,10).generate_password()
    return randon_secret_string


def get_random_produkt_img(img_path):
    img_list = listdir(f"static/img/products/{img_path}/")
    return f"../static/img/products/{img_path}/{choice(img_list)}"

