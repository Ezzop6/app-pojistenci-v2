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
        if self.db.count_documents(login) > 0:
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
        user = self.db.find_one({"_id": ObjectId(user_id)})
        return user["role"]
    
    def get_user_id(self,login):
        user = self.db.find_one({"login": login})
        return user["_id"]
        
    def get_user_data(self, user_id):
        '''Returns user'''
        user = self.db.find_one({"_id": ObjectId(user_id)})
        return user
    
    # def create_fake_users(self, number = 1):
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


usser = DbUsers()
usser.add_user("tsest","test")