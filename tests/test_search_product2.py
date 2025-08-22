"""
AE_API_002 - Validate POST /searchProduct

Checks:
- Status code = 200
- Content-Type = application/json or text/html
- Response is valid JSON
- Response contains matching products (if applicable)
"""

import allure
import pytest
from src.assertions import assert_status, assert_json, assert_header
from src.utils.data_loader import load_json_file
from src.utils.attachments import attach_response

@allure.epic("Products")
@allure.feature("POST /searchProduct")
@pytest.mark.functional
@pytest.mark.parametrize(
    "test_case",
    load_json_file("data/search_products.json"),
    ids=lambda x: x["name"]
)
def test_search_products(client, test_case):
    payload = test_case["payload"]
    name = test_case["name"]

    with allure.step(f"Send POST request to /searchProduct - {name}"):
        resp = client.post("searchProduct", json=payload)
        attach_response(resp, f"searchProduct-{name}")

    with allure.step("Validate response status and headers"):
        assert_status(resp, 200)
        assert_header(resp, "Content-Type", "text/html")  # Adjust if needed

    with allure.step("Validate response body"):
        data = assert_json(resp)
        assert "products" in data or len(data) > 0, "No products found in response"
        allure.attach(str(data), "matched-products", allure.attachment_type.TEXT)
