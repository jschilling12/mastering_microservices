from flask import session
import requests

class OrderClient:
    @staticmethod
    def get_orders():
        headers = {
            'Authorization': 'Basic', + session['user_api_key']
        }
        url = 'http://order-service:5003/api/order'
        response = requests.request(method="GET", url=url, headers=headers)
        orders = response.json()
        return orders

    @staticmethod
    def post_add_to_cart(product_id, qty=1):
        headers = {
            'product_id': product_id,
            'qty': qty,
        }
        url = 'http://order-service:5003/api/order/add-item'
        headers = {
            'Authorization': 'Basic', + session['user_api_key']
        }
        response = requests.request("POST", url=url, data=payload, headers=headers)
        if response:
            order = response.json()
            return order
        
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
        