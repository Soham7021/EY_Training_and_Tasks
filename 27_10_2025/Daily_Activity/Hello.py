import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face API Key from environment variable
API_TOKEN = os.getenv('HUGGINGFACE_API_KEY')

if not API_TOKEN:
    raise ValueError("Hugging Face API key not found in the .env file")

# Test Hugging Face API token validity
test_url = "https://huggingface.co/api/usage"
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(test_url, headers=headers)

if response.status_code == 200:
    print("API token is valid and authorized!")
else:
    print(f"Failed to authenticate: {response.status_code}, {response.text}")
