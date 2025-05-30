#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import requests
import fixtures
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
        mock_get_json.return_value = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }

        client = GithubOrgClient(org_name)
        org_data = client.org
        mock_get_json.assert_called_once_with(
            client.ORG_URL.format(org=org_name)
        )
        self.assertEqual(org_data["name"].lower(), org_name)
        self.assertEqual(
            org_data["repos_url"],
            f"https://api.github.com/orgs/{org_name}/repos"
        )

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the repos_url
        from the org payload. This mocks the org property.
        """
        fake_repos_url = "https://api.github.com/orgs/fake_org/repos"
        client = GithubOrgClient("fake_org")

        # Patch the .org property to return a fake payload
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": fake_repos_url}

            # Access the memoized property
            self.assertEqual(client._public_repos_url, fake_repos_url)
            mock_org.assert_called_once_with()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the list of repo names
        based on the mocked _public_repos_url and get_json payload.
        """
        # setup
        fake_url = "https://api.github.com/orgs/fake_org/repos"
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = fake_payload
        client = GithubOrgClient("fake_org")

        # patch the _public_repos_url property
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_pub_url:
            mock_pub_url.return_value = fake_url

            repos = client.public_repos()

            # assertions
            mock_pub_url.assert_called_once_with()
            mock_get_json.assert_called_once_with(fake_url)
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """
        Test that GithubOrgClient.has_license correctly identifies
        whether a given repo dict contains the specified license key.
        """
        client = GithubOrgClient("irrelevant_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.TEST_PAYLOAD[0][0],
        "repos_payload": fixtures.TEST_PAYLOAD[0][1],
        "expected_repos": fixtures.TEST_PAYLOAD[0][2],
        "apache2_repos": fixtures.TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level patcher for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Side effect function for requests.get
        def side_effect(url):
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.org_payload["repos_url"]:
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            raise ValueError(f"Unexpected URL {url}")

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
