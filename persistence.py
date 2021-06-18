import json


def get_stored_counts():
    f = open("counts.json")
    data = json.load(f)
    f.close()
    return data


def store_counts(**kwargs):
    with open("counts.json", "w") as outfile:
        json.dump(kwargs, outfile)


def log(s):
    with open("log.log", "a") as myfile:
        myfile.write(s + "\n")
