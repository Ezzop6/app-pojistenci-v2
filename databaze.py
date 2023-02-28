from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from customtools.fake_users.user_creator import RandomUser




from customtools.tools import *


class DbConnection:
    def __init__(self):
        '''Connects to database'''
        load_dotenv(find_dotenv())
        password = os.environ.get("MONGODB_PWD")
        my_conection = f"mongodb+srv://ezzop6:{password}@cluster0.qr7l0pg.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(my_conection)
        
class DbUsers(DbConnection):
    def __init__(self):
        super().__init__()
        self.db = self.client.pojistenci_uzivatele.users
        
    def check_if_login_exists(self, login):
        '''Checks if user exists in database'''
        if self.db.count_documents({"login": login}) > 0:
            return True

    def check_if_this_login_exists(self, login):
        '''Checks if user with given login exists in database'''
        if self.db.count_documents({"login": login}) > 0:
            return True
        
    def check_if_password_is_correct(self, login, password):
        '''Checks if password is correct'''
        if self.db.count_documents({"login": login, "password": password}) > 0:
            return True
    
        
    def add_user(self, login,password):
        '''Adds user to database'''
        if not self.check_if_login_exists({"login": login}):
            self.db.insert_one({"login": login, "password": password, "role": "user"})
            print(f"User {login} added")
        else:
            print(f"User {login} already exists")
    
    def get_user_role(self, user_id):
        '''Returns user role'''
        role = self.db.find_one({"_id": ObjectId(user_id)})
        return role["role"]
    
    def get_user_id(self,login):
        id = self.db.find_one({"login": login})
        return id["_id"]
        
    def get_user_data(self, user_id):
        '''Returns user'''
        user = self.db.find_one({"_id": ObjectId(user_id)})
        return user
    
    def update_user_name(self, user_id, name):
        '''Updates user name'''
        self.db.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name}})
        
    def update_user_surname(self, user_id, surname):
        '''Updates user surname'''
        self.db.update_one({"_id": ObjectId(user_id)}, {"$set": {"surname": surname}})
    
    def update_user_birthdate(self, user_id, birthdate):
        '''Updates user birthdate'''
        self.db.update_one({"_id": ObjectId(user_id)}, {"$set": {"birthdate": birthdate}})
        
    def update_user_address(self, user_id, address):
        '''Updates user address'''
        self.db.update_one({"_id": ObjectId(user_id)}, {"$set": {"address": address}})
        
    def create_fake_users(self, number = 1):
        '''Creates fake users'''
        for _ in range(number):
            fake_users = RandomUser().new_user()
            if not self.check_if_login_exists(fake_users["login"]):
                self.db.insert_one(fake_users)
                print(f"User {fake_users} added")

class DbProducts(DbConnection):
    def __init__(self):
        super().__init__()
        self.db = self.client.pojistenci_uzivatele.products
        
    def add_product(self, product):
        '''Adds product to database'''
        self.db.insert_one(product)
        
    def get_all_products(self):
        '''Returns all products'''
        return self.db.find()
    
    def check_if_name_exists(self, product_name):
        '''Checks if product exists'''
        if self.db.count_documents({"name": product_name}) > 0:
            cprint("Product already exists")
            return True
    
    def get_product_by_name(self,produkt_name):
        produkt = self.db.find_one({"name": produkt_name})
        return produkt
    
    def delete_product(self, produkt_name):
        self.db.delete_one({"name": produkt_name})
        
    def get_product_id(self,product_name):
        return self.db.find_one({"name": product_name})["_id"]
    
    def update_product(self,product_name,description,price_per_month):
        cprint(product_name)
        cprint(description)
        cprint(price_per_month)
        self.db.update_one({"name": product_name}, {"$set": {"description": description, "price": price_per_month}})
        
    