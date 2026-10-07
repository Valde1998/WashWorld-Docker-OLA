import unittest
from unittest.mock import patch

from mysql.connector import Error as MySQLError
from werkzeug.security import check_password_hash

from app import app
from demo_user import create_demo_user


class DockerSupportTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.fetch_one", return_value={"ready": 1})
    def test_readiness_checks_database(self, fetch_one):
        response = self.client.get("/health/ready")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ready"})
        fetch_one.assert_called_once_with("SELECT 1 AS ready")

    @patch("app.fetch_one", side_effect=MySQLError("test connection failure"))
    def test_readiness_fails_when_database_fails(self, fetch_one):
        self.assertEqual(self.client.get("/health/ready").status_code, 503)

    @patch("app.fetch_one")
    def test_liveness_does_not_require_database(self, fetch_one):
        self.assertEqual(self.client.get("/").status_code, 200)
        fetch_one.assert_not_called()

    @patch("demo_user.execute")
    @patch("demo_user.fetch_one", return_value=None)
    def test_demo_password_is_hashed(self, fetch_one, execute):
        self.assertEqual(create_demo_user("LocalDemo2026!"), "demo@washworld.invalid")
        values = execute.call_args.args[1]
        self.assertNotEqual(values[3], "LocalDemo2026!")
        self.assertTrue(check_password_hash(values[3], "LocalDemo2026!"))

    @patch("demo_user.execute")
    @patch("demo_user.fetch_one", return_value={"user_id": "existing"})
    def test_demo_user_never_overwrites_existing_account(self, fetch_one, execute):
        with self.assertRaises(ValueError):
            create_demo_user("LocalDemo2026!")
        execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
