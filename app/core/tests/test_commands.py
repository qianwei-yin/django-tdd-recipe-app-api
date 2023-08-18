"""
Test custom Django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# This is a decorator which allows us to 'patch' (which means replace the object) for all test methods that fall within that class.
# When used as a decorator, the object at the namespace provided "core.management.commands.wait_for_db.Command.check" will be replaced with a fake object that is passed as an argument to each of the methods within the class. So in this case, it gets passed as "patched_check" which you will see is available for every method.
@patch("core.management.commands.wait_for_db.Command.check")
class CommandsTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
