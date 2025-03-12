"""
Management command to test the logging configuration.

This command allows you to generate test log messages at different levels
to verify that the logging configuration is working correctly.
"""
import logging
import time
from typing import Any, Dict, List, Optional

from django.core.management.base import BaseCommand, CommandError

from core.logging_utils import (
    get_logger,
    log_api_request,
    log_exception,
    log_user_activity,
)

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """Django management command to test logging configuration."""

    help = "Test the logging configuration by generating log messages at different levels"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--level",
            type=str,
            choices=["debug", "info", "warning", "error", "critical"],
            default="info",
            help="Log level to test (default: info)",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="Number of log messages to generate (default: 1)",
        )
        parser.add_argument(
            "--module",
            type=str,
            default="core.test_logging",
            help="Logger name/module to use (default: core.test_logging)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Test all logging features (basic, API, exception, user activity, forms)",
        )
        parser.add_argument(
            "--forms",
            action="store_true",
            help="Test user forms logging features",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        level = options["level"]
        count = options["count"]
        module = options["module"]
        test_all = options["all"]

        # Get logger for the specified module
        logger = get_logger(module)

        self.stdout.write(
            self.style.SUCCESS(
                f"Testing logging with level={level}, count={count}, module={module}"
            )
        )

        # Basic logging test
        self._test_basic_logging(logger, level, count)

        # Additional tests if --all is specified
        if test_all:
            self._test_api_request_logging(logger)
            self._test_exception_logging(logger)
            self._test_user_activity_logging(logger)
            self._test_forms_logging(logger)
            
        # Test forms logging if --forms is specified
        elif options["forms"]:
            self._test_forms_logging(logger)

        self.stdout.write(
            self.style.SUCCESS(
                f"Logging test completed. Check the log files in the 'logs' directory."
            )
        )

    def _test_basic_logging(
        self, logger: logging.Logger, level: str, count: int
    ) -> None:
        """Test basic logging at the specified level."""
        log_methods = {
            "debug": logger.debug,
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical,
        }

        log_method = log_methods[level]

        self.stdout.write(f"Generating {count} {level.upper()} level log messages...")

        for i in range(1, count + 1):
            log_method(
                f"Test {level.upper()} message {i}/{count} at {time.strftime('%H:%M:%S')}"
            )
            # Small delay to avoid identical timestamps
            time.sleep(0.1)

    def _test_api_request_logging(self, logger: logging.Logger) -> None:
        """Test API request logging."""
        self.stdout.write("Testing API request logging...")

        # Successful API request
        log_api_request(
            logger=logger,
            service_name="TestAPI",
            endpoint="/api/test",
            method="GET",
            status_code=200,
            response_time=0.5,
            request_data={"param1": "value1", "api_key": "secret_key"},
        )

        # Failed API request
        log_api_request(
            logger=logger,
            service_name="TestAPI",
            endpoint="/api/test",
            method="POST",
            status_code=400,
            response_time=0.3,
            request_data={"param1": "invalid", "password": "secret"},
            error="Bad Request: Invalid parameters",
        )

    def _test_exception_logging(self, logger: logging.Logger) -> None:
        """Test exception logging."""
        self.stdout.write("Testing exception logging...")

        try:
            # Simulate a division by zero error
            result = 1 / 0
        except Exception as e:
            log_exception(
                logger=logger,
                exc=e,
                message="Test exception occurred",
                extra={"operation": "division", "value": 0},
            )

    def _test_user_activity_logging(self, logger: logging.Logger) -> None:
        """Test user activity logging."""
        self.stdout.write("Testing user activity logging...")

        # Log user login
        log_user_activity(
            logger=logger,
            user_id=123,
            action="login",
            details={"browser": "Chrome", "platform": "macOS"},
            ip_address="192.168.1.1",
        )

        # Log user action
        log_user_activity(
            logger=logger,
            user_id=123,
            action="create_conversation",
            details={"conversation_id": "abc123", "title": "Test Conversation"},
            ip_address="192.168.1.1",
        )
        
    def _test_forms_logging(self, logger: logging.Logger) -> None:
        """Test user forms logging."""
        self.stdout.write("Testing user forms logging...")
        
        # Simulate successful login
        logger.info(
            f"Successful login for user: test_user",
            extra={
                'username': 'test_user',
                'user_id': 42,
                'action': 'login_success'
            }
        )
        
        # Simulate failed login with incorrect password
        logger.warning(
            f"Failed login attempt for username: test_user (incorrect password)",
            extra={
                'username': 'test_user',
                'action': 'login_failed',
                'reason': 'incorrect_password'
            }
        )
        
        # Simulate failed login with non-existent user
        logger.warning(
            f"Failed login attempt for non-existent username: fake_user",
            extra={
                'username': 'fake_user',
                'action': 'login_failed',
                'reason': 'user_not_found'
            }
        )
        
        # Simulate user registration
        logger.info(
            f"New user registered: new_user",
            extra={
                'user_id': 100,
                'username': 'new_user',
                'email': 'new_user@example.com',
                'action': 'user_registration'
            }
        )
        
        # Simulate profile update
        logger.info(
            f"User test_user updated profile fields: email, first_name, bio",
            extra={
                'user_id': 42,
                'username': 'test_user',
                'updated_fields': ['email', 'first_name', 'bio'],
                'action': 'profile_update'
            }
        )
        
        # Simulate profile picture upload failure
        logger.warning(
            f"User test_user attempted to upload oversized profile picture",
            extra={
                'user_id': 42,
                'username': 'test_user',
                'file_size': 6291456,  # 6MB
                'max_size': 5242880,   # 5MB
                'action': 'profile_picture_upload_failed'
            }
        )
