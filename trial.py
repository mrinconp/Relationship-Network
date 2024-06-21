import json

with open("info.json","r") as file:
    data = json.load(file)
    print(len(data["cities"]))