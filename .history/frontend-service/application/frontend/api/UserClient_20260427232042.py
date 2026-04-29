import requests


class UserClient:
    @staticmethod
    def post_login():
        """Call user-service login with default demo credentials and return api_key.

        Matches the expected REPL usage:
          >>> from application.frontend.api.UserClient import UserClient
          >>> UserClient.post_login()
        """
        api_key = False
        payload = {
            "username": "johnny",
            "password": "depp",
        }
        # user-service runs on port 5001 (per run.py and container mapping)
        url = "http://user-service:5001/api/user/login"
        # Backend reads request.form, so send form-encoded data
        response = requests.post(url, data=payload)
        if response and response.headers.get("content-type", "").startswith("application/json"):
            d = response.json()
            if d.get("api_key") is not None:
                api_key = d["api_key"]
        return api_key