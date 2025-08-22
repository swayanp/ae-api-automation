import pytest
import allure
from src.assertions import assert_status
from src.utils.attachments import attach_response


@allure.epic("Products")
@allure.feature("GET /productsList")
@pytest.mark.functional
class TestGetSingleProduct:
    
    @allure.title("Validate product with ID=1 exists in /productsList")
    @allure.description("This test fetches all products and checks if product_id=1 is present with correct attributes.")
    def test_get_single_product_details(self, client):
        endpoint = "productsList"

        with allure.step(f"Send GET request to /{endpoint}"):
            response = client.get(endpoint)
            attach_response(response, endpoint)

        with allure.step("Validate response status code is 200"):
            assert_status(response, 200)

        with allure.step("Filter product by ID and assert details"):
            products = response.json().get("products", [])
            target = next((p for p in products if str(p["id"]) == "1"), None)

            assert target is not None, "❌ Product with ID=1 not found"
            assert "name" in target, "❌ Product name missing"
            assert isinstance(target["name"], str), "❌ Product name should be string"
            assert len(target["name"]) > 0, "❌ Product name is empty"
