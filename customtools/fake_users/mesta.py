from random import randint,choice


city = "./customtools/fake_users/jmena/city.txt"
street = "./customtools/fake_users/jmena/street.txt"



class FakeCity:
    def __init__(self) -> None:
        pass
        
    def get_city(self):
        with open (city,"r",encoding="utf8") as file:
            name = choice(file.readlines())
        return name.strip()
    
    def get_street(self):
        with open (street,"r",encoding="utf8") as file:
            name = choice(file.readlines())
        return name.strip()
    
    def get_street_number(self):
        street_number = str(randint(1,1000))+"/"+str(randint(1,1000))
        return street_number
    
    def get_zip_code(self):
        first_number = str(randint(1,7))
        zip_code = str(randint(1000,9999))
        return first_number + zip_code
    
    def get_full_address(self):
        self.city = self.get_city()
        self.street = self.get_street()
        self.street_number = self.get_street_number()
        self.zip_code = self.get_zip_code()
        return self.__dict__
