import logging
from pathlib import Path

# Define the logging directory
log_dir = Path(__file__).resolve().parent
log_dir.mkdir(exist_ok=True)

# Log file paths inside logging_systems
app_log = log_dir / "app.log"
error_log = log_dir / "error.log"

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# App logger
app_handler = logging.FileHandler(app_log)
app_handler.setFormatter(formatter)
app_handler.setLevel(logging.INFO)

# Error logger
error_handler = logging.FileHandler(error_log)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

# Main logger
logger = logging.getLogger("supply_chain_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(app_handler)
logger.addHandler(error_handler)
