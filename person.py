import random
import json

class Person():
    def __init__(self):
        with open("info.json","r") as file:
            data = json.load(file)
            self.first_name = random.choice(data["first_names"])
            self.last_name = random.choice(data["last_names"])
            self.age = random.randint(18,60)
            self.city = random.choice(data["cities"])
            self.job = random.choice(data["jobs"])
            
            self.id = ".".join([str(data["first_names"].index(self.first_name)),
                       str(data["last_names"].index(self.last_name)),
                       str(data["cities"].index(self.city)),
                       str(data["jobs"].index(self.job))])
            
    def show_attributes(self):
        print({"first_name": self.first_name,
                "last_name": self.last_name,
                "age": self.age,
                "city": self.city,
                "job": self.job,
                "id": self.id})