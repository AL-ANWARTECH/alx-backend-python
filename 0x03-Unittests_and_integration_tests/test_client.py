#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient and integration tests.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org."""
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"org": org_name})
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            client = GithubOrgClient("google")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


# Integration Tests
@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos,
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure the mock to return different payloads based on the URL
        mock_get.side_effect = lambda url: MockResponse(url)

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()


class MockResponse:
    """Helper mock response class for integration tests."""

    def __init__(self, url):
        self.url = url

    def json(self):
        if "repos" in self.url:
            return repos_payload
        return org_payload


if __name__ == "__main__":
    unittest.main()
