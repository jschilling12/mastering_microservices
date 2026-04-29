from flask import session
import requests


class OrderClient:
    @staticmethod
    def get_orders():
        url = 'http://order-service:5003/api/order'
        # Requires an active Flask request context to access session
        api_key = session.get('user_api_key')
        headers = {
            'Authorization': f'Basic {api_key}'
        } if api_key else {}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post_add_to_cart(product_id, qty=1):
        url = 'http://order-service:5003/api/order/add-item'
        api_key = session.get('user_api_key')
        headers = {
            'Authorization': f'Basic {api_key}'
        } if api_key else {}

        payload = {
            'product_id': product_id,
            'qty': qty,
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
        
    @staticmethod
    def post_checkout():
        url = 'http://order-service:5003/api/order/checkout'
        headers =   {
            'Authorization': 'Basic', + session['user_api_key']
        }
        response = requests.request("POST", url=url, headers=headers)
        if response:
            order = response.json()
            return order
        