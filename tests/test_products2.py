import allure
import pytest
from src.assertions import assert_status, assert_json, assert_header
from src.utils.attachments import attach_response


@allure.epic("Products")
@allure.feature("GET /productsList")
@pytest.mark.smoke
def test_get_products_list(client):
    with allure.step("Send GET request to /productsList"):
        resp = client.get("productsList")
        attach_response(resp, "productsList")

    with allure.step("Validate response status and headers"):
        assert_status(resp, 200)
        assert_header(resp, "Content-Type", "text/html")

    with allure.step("Validate JSON body"):
        data = assert_json(resp)
        assert "products" in data, "Missing 'products' key in response"
        assert len(data["products"]) > 0, "No products found in response"
