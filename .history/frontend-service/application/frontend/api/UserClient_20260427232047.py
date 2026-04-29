import requests

class UserClient:
    @staticmethod
    def post_login(form):
        api_key = False
        payload = {
            "username": 'johnny',
            "password": 'depp'
            }
        url = 'http://user-service:5000/api/user/login'
        response = requests.request("POST", url=url, json=payload)
        if response:
            d = response.json()
            if d['api_key'] is not None:
                api_key = d['api_key']
        return api_key