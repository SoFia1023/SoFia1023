"""
Tests for the settings module configuration.

This module tests the environment selection logic and environment variable loading
in the settings module.
"""
import os
from unittest import mock
import pytest
from django.conf import settings
from django.test import override_settings


@pytest.mark.parametrize(
    "django_env,expected_module",
    [
        ("development", "inspireIA.settings.development"),
        ("production", "inspireIA.settings.production"),
        ("testing", "inspireIA.settings.testing"),
        # Default to development for unknown values
        ("unknown", "inspireIA.settings.development"),
    ],
)
def test_environment_selection(django_env, expected_module):
    """
    Test that the correct settings module is selected based on DJANGO_ENV.
    
    Args:
        django_env: The value of DJANGO_ENV environment variable
        expected_module: The expected settings module to be imported
    """
    with mock.patch.dict(os.environ, {"DJANGO_ENV": django_env}):
        # We need to reload the settings module to test different environments
        with mock.patch("importlib.import_module") as mock_import:
            # This is a bit of a hack to test the import logic without actually
            # reloading Django settings, which would be complex in a test
            from inspireIA.settings import __init__ as settings_init
            
            # Force reload of the module
            reload_module = getattr(settings_init, "__reload__", None)
            if reload_module:
                reload_module()
            
            # Check if the correct module was imported
            for call in mock_import.call_args_list:
                args, _ = call
                if args[0] == expected_module:
                    break
            else:
                pytest.fail(f"Expected module {expected_module} was not imported")


def test_get_env_value():
    """Test the get_env_value helper function."""
    from inspireIA.settings import get_env_value
    
    # Test with existing environment variable
    with mock.patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        assert get_env_value("TEST_VAR") == "test_value"
        assert get_env_value("TEST_VAR", "default") == "test_value"
    
    # Test with non-existing environment variable
    assert get_env_value("NON_EXISTENT_VAR") is None
    assert get_env_value("NON_EXISTENT_VAR", "default") == "default"


@pytest.mark.django_db
def test_database_configuration():
    """Test that the database is configured correctly."""
    # This test will use the testing settings by default in pytest
    assert "default" in settings.DATABASES
    
    # In testing environment, we should use an in-memory SQLite database
    if os.environ.get("DJANGO_ENV") == "testing":
        assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
        assert settings.DATABASES["default"]["NAME"] == ":memory:"


@pytest.mark.parametrize(
    "debug_value,expected",
    [
        ("True", True),
        ("true", True),
        ("Yes", True),
        ("y", True),
        ("1", True),
        ("False", False),
        ("false", False),
        ("No", False),
        ("n", False),
        ("0", False),
    ],
)
def test_boolean_env_parsing(debug_value, expected):
    """
    Test that boolean environment variables are parsed correctly.
    
    Args:
        debug_value: The string value of the DEBUG environment variable
        expected: The expected boolean value after parsing
    """
    with mock.patch.dict(os.environ, {"DEBUG": debug_value, "DJANGO_ENV": "development"}):
        # We need to reload the settings module to test different DEBUG values
        with override_settings():
            # Force reload of the development settings
            from importlib import reload
            from inspireIA.settings import development
            
            reload(development)
            
            # Check if DEBUG was set correctly
            assert development.DEBUG is expected


def test_allowed_hosts_parsing():
    """Test that ALLOWED_HOSTS is parsed correctly from environment variables."""
    test_hosts = "example.com,test.com,localhost"
    expected = ["example.com", "test.com", "localhost"]
    
    with mock.patch.dict(os.environ, {"ALLOWED_HOSTS": test_hosts, "DJANGO_ENV": "development"}):
        # We need to reload the settings module to test different ALLOWED_HOSTS values
        with override_settings():
            # Force reload of the development settings
            from importlib import reload
            from inspireIA.settings import development
            
            reload(development)
            
            # Check if ALLOWED_HOSTS was set correctly
            assert development.ALLOWED_HOSTS == expected


def test_dotenv_loading():
    """Test that environment variables are loaded from .env file."""
    # Create a mock .env file content
    mock_env_content = """
    TEST_VAR=test_value
    ANOTHER_VAR=another_value
    """
    
    # Mock the open function to return our mock .env content
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_env_content)):
        # Mock os.path.exists to return True for .env file
        with mock.patch("os.path.exists", return_value=True):
            # Mock load_dotenv to actually set the environment variables
            with mock.patch("dotenv.load_dotenv") as mock_load_dotenv:
                mock_load_dotenv.side_effect = lambda *args, **kwargs: os.environ.update({
                    "TEST_VAR": "test_value",
                    "ANOTHER_VAR": "another_value"
                })
                
                # Reload the settings module
                from importlib import reload
                from inspireIA.settings import __init__ as settings_init
                
                reload(settings_init)
                
                # Check if the environment variables were loaded
                assert os.environ.get("TEST_VAR") == "test_value"
                assert os.environ.get("ANOTHER_VAR") == "another_value"
