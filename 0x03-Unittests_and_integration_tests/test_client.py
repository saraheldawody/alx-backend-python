#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        This method uses parameterized tests to check that the org method
        returns the expected organization data without making external HTTP calls.
        """
        mock_get_json.return_value = {"name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        client = GithubOrgClient(org_name)
        org_data = client.org
        mock_get_json.assert_called_once_with(client.ORG_URL.format(org=org_name))
        self.assertEqual(org_data["name"].lower(), org_name)
        self.assertEqual(org_data["repos_url"], f"https://api.github.com/orgs/{org_name}/repos")

if __name__ == '__main__':
    unittest.main()