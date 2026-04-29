from flask import session
import requests

class UserClient:
    @staticmethod
    def post_login(form):
        api_key = False
        payload = {
            "username": form.username.data,
            "password": form.password.data
            }
        url = 'http://user-service:5000/api/user/login'
        response = requests.request("POST", url=url, json=payload)
        if response:
            d = response.json()
            if d['api_key'] is not None:
                api_key = d['api_key']
        return api_key
    
    @staticmethod
    def get_user():
        api_key = session.get('user_api_key')
        headers = {
            'Authorization': f'Basic {api_key}'
        } if api_key else {}
        url = 'http://user-service:5000/api/user'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def post_user_create(form):
        user = False
        payload = {
            'email': form.email.data,
            'username': form.username.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'password': form.password.data
        }
        url = 'http://user-service:5000/api/user/create'
        response = requests.request("POST", url=url, json=payload)
        if response:
            user = response.json()
        return user
    
    @staticmethod
    def does_exist(username):
        url = f'http://user-service:5000/api/user/' + username + '/exists'
        response = requests.request("GET", url=url)
        return response.status_code == 200
    
    