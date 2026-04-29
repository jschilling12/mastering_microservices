import os
import requests


class UserClient:
    @staticmethod
    def post_login(username: str, password: str) -> str | None:
        """Log in to user-service and return api_key or None on failure.

        Notes:
        - user-service expects form-encoded fields (request.form), not JSON.
        - Default base URL can be overridden with USER_SERVICE_URL env var.
          Examples:
            USER_SERVICE_URL=http://localhost:5001 (local run)
            USER_SERVICE_URL=http://user-service:5001 (Docker network)
        """

        base_url = os.getenv("USER_SERVICE_URL", "http://localhost:5001")
        url = f"{base_url.rstrip('/')}/api/user/login"

        # Send as form data to match backend's request.form usage
        payload = {"username": username, "password": password}
        try:
            resp = requests.post(url, data=payload, timeout=10)
        except requests.RequestException:
            return None

        if not resp.ok:
            return None

        try:
            data = resp.json()
        except ValueError:
            return None

        return data.get("api_key")