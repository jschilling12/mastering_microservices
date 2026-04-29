import requests

class UerClient:
    @staticmethod
    def get_user(api_key):
        headers = {
            'Authorization': api_key
            
