from random import randint, choice
from datetime import datetime, timedelta
from customtools.password_generator import PasswordGenerator
from customtools.fake_users.cznames import CzNames
from customtools.fake_users.mesta import FakeCity


class RandomUser:
    '''Třída pro vytvoření náhodného uživatele jo vim je to dost CzechEnglish 
    ale uz to nechci prepisovat'''
    def __init__(self, gender = None):
        self.gender = gender
        if self.gender == None:
            self.gender = choice((True,False))
        self.role = "user"

    def vyber_jmeno(self):
        full_name =  CzNames(self.gender)
        self.name = full_name.first_name
        self.surname = full_name.surname
        
    def vyber_datum_narozeni(self):
        start_date = datetime.strptime("1950-01-01", "%Y-%m-%d")
        end_date = datetime.now()
        delta = end_date - start_date
        random_delta = timedelta(days=randint(0, delta.days))
        random_date = start_date + random_delta
        self.birth_date = random_date.strftime("%Y.%m.%d")

    def nastav_rodne_cislo(self):
        year = self.birth_date[0:4]
        month = self.birth_date[5:7]
        day = self.birth_date[8:10]
        if not self.gender: year = str(int(year) + 50)
        if int(year) < 1954:
            self.birth_number = "".join([year[2:],month,day,"/",str(randint(1,1000)).zfill(3)])
        else:
            self.birth_number = "".join([year[2:],month,day])
            while len(self.birth_number) < 10:
                num = str(randint(1, 10000)).zfill(4)
                if int(self.birth_number + num) % 11 == 0:
                    self.birth_number =  "".join([self.birth_number,"/",num])

    def nastav_heslo(self):
        self.password = PasswordGenerator().generate_password()
        
    def nastav_adresu(self):
        self.city = FakeCity().get_city()
        self.street = FakeCity().get_street()
        self.street_number = FakeCity().get_street_number()
        self.zip_code = FakeCity().get_zip_code()
        
    def nastav_email(self):
        from unidecode import unidecode
        with open ("./customtools/fake_users/jmena/email.txt","r",encoding="utf8") as file:
            provider = choice(file.readlines())
        name_without_diacritics = unidecode(self.name).lower()
        surname_without_diacritics = unidecode(self.surname).lower()
        self.email = f"{name_without_diacritics}{surname_without_diacritics}@{provider.strip()}"
        
    def nastav_telefon(self):
        operator = choice((601,602,606,607,702,720,603,604,605,608,770,777))
        self.phone_number = f"+420 {operator} {str(randint(0,999)).zfill(3)} {str(randint(0,999)).zfill(3)}"
        
    def nastav_login(self):
        self.login = f"{self.name}{self.surname[0]}{self.birth_date[8:10]}"
        
        
    def new_user(self):
        '''Vytvoří nového uživatele a vrátí jeho slovník'''
        self.vyber_jmeno()
        self.vyber_datum_narozeni()
        self.nastav_rodne_cislo()
        self.nastav_heslo()
        self.nastav_adresu()
        self.nastav_email()
        self.nastav_telefon()
        self.nastav_login()
        return self.__dict__
