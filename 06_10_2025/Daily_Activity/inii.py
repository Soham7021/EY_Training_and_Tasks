import configparser

config = configparser.ConfigParser()

config['database'] = {
    "host": "localhost",
    "port" : 3306,
    "user" : "root",
    "password" : "admin123",
}

with open('app.ini.json', 'w') as configfile:
    config.write(configfile)

config.read("app.ini")
print(config["database"]["host"])
print(config["database"]["port"])