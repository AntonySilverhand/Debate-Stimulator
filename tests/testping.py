import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get proxy settings from environment variables
http_proxy = os.getenv("http_proxy")
https_proxy = os.getenv("https_proxy")

# Prepare proxies dictionary only if settings are found
proxies = None
if http_proxy or https_proxy:
    proxies = {}
    if http_proxy:
        proxies['http'] = http_proxy
    if https_proxy:
        proxies['https'] = https_proxy
    print(f"Using proxies: {proxies}")
else:
    print("No proxy settings found in environment.")

try:
    print("Attempting to connect to Google...")
    # Pass the proxies dictionary (or None) to requests
    response = requests.get("https://www.google.com", proxies=proxies, timeout=10) # Added timeout
    print(f"Google Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error connecting to Google: {e}")

