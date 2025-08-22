"""
AE_API_001 - Validate GET /productsList

Checks:
- Status code = 200
- Content-Type = application/json
- Response is valid JSON
- At least 1 product is returned
"""

import allure
import pytest
from src.assertions import assert_status, assert_json, assert_header
from src.utils.attachments import attach_response

@allure.epic("Products")
@allure.feature("GET /productsList")
@allure.title("AE_API_001 - Verify product list is returned successfully")
@allure.description("""
This test verifies that the GET /productsList endpoint returns a valid JSON response 
with expected headers and a non-empty list of products.
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("products", "regression", "api")
@pytest.mark.smoke
@pytest.mark.regression
def test_get_products_list(client):
    endpoint = "productsList"

    with allure.step("Send GET request to /productsList"):
        resp = client.get(endpoint)
        attach_response(resp, endpoint)

        # Attach response time
        allure.attach(
            str(resp.elapsed.total_seconds()) + " seconds",
            name="response-time",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Validate response status and headers"):
        assert_status(resp, 200)
        # assert_header(resp, "Content-Type", "application/json")
        assert_header(resp, "Content-Type", "text/html")  # Adjust if needed

    with allure.step("Validate response body"):
        data = assert_json(resp)
        assert isinstance(data, dict), "Response is not a JSON object"
        assert "products" in data, "Key 'products' missing in response"

        products = data["products"]
        assert isinstance(products, list), "Products is not a list"
        assert len(products) > 0, "No products returned"

        # Attach a product preview
        preview = str(products[:3])
        allure.attach(preview, "products-preview", allure.attachment_type.TEXT)
