"""
conftest.py
------------
Pytest configuration file that provides shared fixtures and command-line options.

Features:
- Supports --env flag to switch between dev, qa, prod
- Loads environment config from settings.yaml
- Injects logger and APIClient into every test
- Automatically attaches request/response to Allure report
- Tags each test in Allure with the active environment
"""

import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import yaml
import allure
from src.api_client import APIClient
from src.utils.logger import get_logger

def pytest_addoption(parser):
    """
    Adds a custom command-line flag to pytest: --env
    """
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment: dev | qa | prod"
    )

@pytest.fixture(scope="session")
def target_env(pytestconfig):
    """
    Reads the --env value from CLI and returns it (default = dev)
    """
    return pytestconfig.getoption("--env").lower()

@pytest.fixture(scope="session")
def logger():
    """
    Creates a shared logger for the entire test session.
    """
    return get_logger("AE.API")

@pytest.fixture(scope="session")
def client(target_env, logger):
    """
    Builds an APIClient using base_url from settings.yaml based on selected environment.
    """
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    env_config = cfg.get("envs", {}).get(target_env)
    if not env_config:
        raise pytest.UsageError(f"Invalid --env '{target_env}'. Use one of: {list(cfg.get('envs').keys())}")

    base_url = env_config["base_url"]
    logger.info(f"[ENV={target_env}] Using base URL: {base_url}")

    return APIClient(base_url=base_url)

# @pytest.fixture
# def attach_response():
#     """
#     Fixture to attach request and response details to Allure report.
#     """
#     def _attach(response, name="response"):
#         try:
#             allure.attach(
#                 f"{response.request.method} {response.request.url}",
#                 name + "-request",
#                 allure.attachment_type.TEXT
#             )
#             allure.attach(
#                 str(response.request.headers),
#                 name + "-request-headers",
#                 allure.attachment_type.TEXT
#             )
#             allure.attach(
#                 response.text,
#                 name + "-response-body",
#                 allure.attachment_type.JSON if "application/json" in response.headers.get("Content-Type", "") else allure.attachment_type.TEXT
#             )
#         except Exception as e:
#             print(f"⚠️ Failed to attach response to Allure: {e}")
#     return _attach

@pytest.fixture(autouse=True)
def label_env_in_allure(target_env):
    """
    Auto-label every test in Allure with the active environment.
    """
    allure.dynamic.label("env", target_env)
