import pytest
import allure
import json
from src.assertions import assert_status, assert_header
from src.utils.data_loader import load_json_file
from src.utils.attachments import attach_response

@allure.epic("Products")
@allure.feature("POST /searchProduct")
@pytest.mark.functional
class TestSearchProduct:

    @pytest.mark.parametrize("test_case", load_json_file("data/search_products.json"), ids=lambda x: x["name"])
    def test_search_product(self, client, test_case):
        payload = test_case["payload"]

        with allure.step(f"Send POST request to /searchProduct with payload: {payload}"):
            resp = client.post("searchProduct", data=payload)
            attach_response(resp, "searchProduct")

        with allure.step("Validate status code and Content-Type header"):
            assert_status(resp, test_case["expected_status"])
            assert_header(resp, "Content-Type", "text/html")
