import requests

class UerClient:
    @staticmethod
    def get_user(api_key):
        headers = {
            'Authorization': api_key
        }
        response = requests.request(method="GET", url='http://user-service:5001/api/user', headers=headers)
        if response.status_code == 401:
            return False
        return response.json()
