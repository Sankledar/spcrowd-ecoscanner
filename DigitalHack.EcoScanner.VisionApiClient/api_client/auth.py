import google.cloud
from google.cloud.client import Client
def get_Api_client():
    
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = Client.from_service_account_json('api_client\\Eco-smth-9e5ce2960c50.json')

    # Make an authenticated API request
    return storage_client