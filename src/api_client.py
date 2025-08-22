"""
api_client.py
--------------
This file defines the APIClient class, which handles all HTTP requests to the API server.

Features:
- Reads base URL, timeout, retry settings from `config/settings.yaml`
- Uses the `requests` library to send HTTP requests
- Uses `tenacity` to retry requests if they fail (e.g., due to network issues)
- Provides convenient methods: .get(), .post(), .put(), .delete()
- Automatically adds headers like Accept, User-Agent
- Supports environment-based switching (dev/qa/prod) via settings

This client is used in all test files via the `client` fixture.
"""

import os
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

# Load configuration from YAML file
def _load_settings():
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)  # Parse YAML into Python dictionary

    # Determine environment (default = dev)
    env = os.getenv("ENV", "dev").lower()

    # Get base_url from env-specific config
    env_cfg = cfg.get("envs", {}).get(env, {})
    base_url = env_cfg.get("base_url", "https://automationexercise.com/api")

    # Load timeout and retry settings from default config
    timeout = cfg["default"].get("timeout", 10)
    retries = cfg["default"].get("retries", 2)
    backoff = cfg["default"].get("retry_backoff", 0.2)

    return base_url.rstrip("/"), timeout, retries, backoff

# Load settings once at module level
BASE_URL, TIMEOUT, RETRIES, BACKOFF = _load_settings()

class APIClient:
    """
    A reusable HTTP client to make GET, POST, PUT, DELETE requests to the target API.
    Adds retry, timeout, and default headers.
    """

    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()  # Creates a reusable session (efficient for multiple requests)

        # Add default headers for all requests
        self.session.headers.update({
            "Accept": "application/json, */*;q=0.5",
            "User-Agent": "AE-API-Automation/1.0"
        })

    def _url(self, path: str) -> str:
        """
        Helper method to join base_url with endpoint path.
        """
        return f"{self.base_url}/{path.lstrip('/')}"

    @retry(
        stop=stop_after_attempt(RETRIES),
        wait=wait_exponential_jitter(initial=BACKOFF, max=2)
    )
    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        Core request method (with retry). Can be used directly or via .get/.post wrappers.
        """
        return self.session.request(
            method=method.upper(),
            url=self._url(path),
            timeout=self.timeout,
            **kwargs  # This can include json=, data=, headers=, etc.
        )

    # Shortcut methods for GET, POST, PUT, DELETE
    def get(self, path, **kw): return self.request("GET", path, **kw)
    def post(self, path, **kw): return self.request("POST", path, **kw)
    def put(self, path, **kw): return self.request("PUT", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)

# resp = client.get("productsList")
# resp = client.post("searchProduct", json=payload)

