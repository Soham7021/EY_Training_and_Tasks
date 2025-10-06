import logging

import yaml

logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

config = {
    "app":{
        "name": "Student Portal",
        "version": 1.0
    },
    "database": {
        "host": "localhost",
        "port": 3306,
        "user": "root"
    }
}

with open("config.yaml", "w") as f:
    yaml.dump(config, f)
try:
    with open("config.yaml", "r") as f:

        data = yaml.safe_load(f)
        host = data["database"]["host"]
        port = data["database"]["port"]
        user = data["database"]["user"]
        print(f"Connecting to {host}:{port} as {user}")
        logging.info("Config loaded successfully.")

except Exception as e:
    logging.error("File not found")
