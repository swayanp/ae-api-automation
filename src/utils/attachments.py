"""
attachments.py
---------------
This utility provides reusable functions to attach API request/response details
to Allure reports in a structured and consistent way.
"""

import allure
import json


def attach_response(response, name: str = "response"):
    """
    Attaches the request and response info to the Allure report.

    Args:
        response (requests.Response): The response object
        name (str): A label used to prefix attachments (like the endpoint name)
    """
    # Request URL
    allure.attach(
        response.request.url,
        name=f"{name}-request",
        attachment_type=allure.attachment_type.TEXT
    )

    # Request headers
    headers = "\n".join(f"{k}: {v}" for k, v in response.request.headers.items())
    allure.attach(
        headers,
        name=f"{name}-request-headers",
        attachment_type=allure.attachment_type.TEXT
    )

    # Response body
    content_type = response.headers.get("Content-Type", "").lower()
    if "application/json" in content_type or "text/html" in content_type:
        try:
            formatted = json.dumps(response.json(), indent=2)
            attachment_type = allure.attachment_type.JSON
        except Exception:
            formatted = response.text
            attachment_type = allure.attachment_type.TEXT
    else:
        formatted = response.text
        attachment_type = allure.attachment_type.TEXT

    allure.attach(
        formatted,
        name=f"{name}-response-body",
        attachment_type=attachment_type
    )
