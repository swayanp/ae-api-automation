import pytest
import allure
from src.assertions import assert_status, assert_in_body
from src.utils.attachments import attach_response

@allure.epic("Brands")
@allure.feature("GET /brandsList")
@pytest.mark.functional
@pytest.mark.smoke
def test_get_brands_list(client):
    with allure.step("Send GET request to /brandsList"):
        resp = client.get("brandsList")
        attach_response(resp, "brandsList")

    with allure.step("Validate response status code"):
        assert_status(resp, 200)

    with allure.step("Check known brand in response body (e.g., Polo)"):
        assert_in_body(resp, "Polo")
