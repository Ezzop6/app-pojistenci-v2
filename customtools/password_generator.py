from random import shuffle,choice

class PasswordGenerator:
    def __init__(self,small_letters = 3,big_letters = 3,digits = 2,special_character = 4):
        self.character_small = "abcdefghijklmnopqrstuvwxyz"
        self.character_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.character_digit = "0123456789"
        self.character_special = "!@#$%^&*()_+"
        self.small_letters = small_letters
        self.big_letters = big_letters
        self.digits = digits
        self.special_character = special_character
        self.generate_password()

        
    def generate_password(self):
        self.password = [ choice(self.character_small) for i in range(self.small_letters)]
        self.password += [ choice(self.character_big) for i in range(self.big_letters)]
        self.password += [ choice(self.character_digit) for i in range(self.digits)]
        self.password += [ choice(self.character_special) for i in range(self.special_character)]
        shuffle(self.password)
        self.password = "".join(self.password)
        return self.password
