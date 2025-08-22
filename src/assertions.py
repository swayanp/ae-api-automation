"""
assertions.py
--------------
Reusable assertion helpers to validate API responses in a modular and Allure-enhanced way.

Features:
- assert_status(): Verify HTTP status code with Allure step
- assert_header(): Validate headers with clear error on mismatch
- assert_json(): Parse response as JSON, fail with body preview
- assert_schema(): Validate JSON response using a schema
- assert_in_body(): Check if plain/text HTML body contains expected text
"""

import allure
from jsonschema import validate


def assert_status(response, expected=200):
    with allure.step(f"Assert status code == {expected}"):
        actual = response.status_code
        # allure.attach(
        #     str(actual),
        #     name="actual-status-code",
        #     attachment_type=allure.attachment_type.TEXT
        # )
        if actual != expected:
            allure.attach(
                response.text,
                name="failure-response-body",
                attachment_type=allure.attachment_type.TEXT
            )
        assert actual == expected, f"❌ Expected status {expected}, but got {actual}. Body: {response.text[:300]}"


def assert_header(response, header_name, expected_contains=None):
    """
    Asserts that a specific header exists in the response and optionally contains an expected value.
    Args:
        response: The response object containing headers.
        header_name (str): The name of the header to check.
        expected_contains (str, optional): A string that should be contained in the header value. If provided, the function will assert that the header value contains this string.
    Raises:
        AssertionError: If the header is missing or does not contain the expected value.
    """
    with allure.step(f"Assert header '{header_name}' exists"):
        headers = response.headers
        assert header_name in headers, f"❌ Missing header: {header_name}"

    if expected_contains:
        with allure.step(f"Assert header '{header_name}' contains '{expected_contains}'"):
            value = headers[header_name]
            allure.attach(
                value,
                name=f"{header_name}-value",
                attachment_type=allure.attachment_type.TEXT
            )
            assert expected_contains in value, f"❌ Header {header_name} does not contain expected value: '{expected_contains}'"


def assert_json(response):
    with allure.step("Assert response is valid JSON"):
        allure.attach(
            response.text,
            name="raw-response-body",
            attachment_type=allure.attachment_type.TEXT
        )
        # Will raise if not JSON – fail fast
        parsed = response.json()
        allure.attach(
            str(parsed)[:500],
            name="parsed-json-preview",
            attachment_type=allure.attachment_type.JSON
        )
        return parsed


def assert_schema(instance: dict, schema: dict):
    with allure.step("Validate JSON schema"):
        validate(instance=instance, schema=schema)


def assert_in_body(response, expected: str):
    with allure.step(f"Assert body contains: '{expected}'"):
        allure.attach(
            response.text,
            name="full-body-preview",
            attachment_type=allure.attachment_type.TEXT
        )
        assert expected in response.text, f"❌ Response body does not contain: {expected}"
