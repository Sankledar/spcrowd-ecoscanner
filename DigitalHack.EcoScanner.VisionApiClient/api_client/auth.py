import google.cloud
import os
from google.cloud.client import Client
def get_Api_client():
    
    # Explicitly use service account credentials by specifying the private key
    # file.
    curdir = os.path.dirname(os.path.abspath(__file__))
    storage_client = Client.from_service_account_json(os.path.join(curdir,'Eco-smth-9e5ce2960c50.json'))

    # Make an authenticated API request
    return storage_client