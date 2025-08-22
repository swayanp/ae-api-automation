"""
AE_API_005 - Validate GET /categories

Checks:
- Status code = 200
- Content-Type = application/json or text/html
- Response is valid JSON
- At least 1 category is returned (or relevant key exists)
"""

import allure
import pytest
from src.assertions import assert_status, assert_json, assert_header
from src.utils.attachments import attach_response

@allure.epic("Products")
@allure.feature("GET /categories")
@pytest.mark.smoke
@pytest.mark.functional
def test_get_categories(client):
    endpoint = "categories"

    with allure.step("Send GET request to /categories"):
        resp = client.get(endpoint)
        attach_response(resp, endpoint)

    with allure.step("Validate response status and headers"):
        assert_status(resp, 200)
        assert_header(resp, "Content-Type", "text/html")  # adjust if it changes

    with allure.step("Validate response body"):
        data = assert_json(resp)
        assert isinstance(data, dict), "Response is not a JSON object"

        # Try validating categories key
        possible_keys = ["categories", "category_list"]
        assert any(key in data for key in possible_keys), "No category key found in response"

        found_key = next((k for k in possible_keys if k in data), None)
        categories = data[found_key]
        assert isinstance(categories, list), "Categories is not a list"
        assert len(categories) > 0, "No categories found"

        # Optionally attach preview
        allure.attach(str(categories[:3]), "categories-preview", allure.attachment_type.TEXT)
