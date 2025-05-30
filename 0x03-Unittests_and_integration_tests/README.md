# 0x03. Unittests and Integration Tests

This folder contains unit and integration tests for Python utility and client modules, focusing on parameterization, mocking, patching, and integration testing.

## Table of Contents

- [Overview](#overview)
- [Tasks and Implementation](#tasks-and-implementation)
  - [0. Parameterize a unit test](#0-parameterize-a-unit-test)
  - [1. Parameterize a unit test (Exception)](#1-parameterize-a-unit-test-exception)
  - [2. Mock HTTP calls](#2-mock-http-calls)
  - [3. Parameterize and patch](#3-parameterize-and-patch)
  - [4. Parameterize and patch as decorators](#4-parameterize-and-patch-as-decorators)
  - [5. Mocking a property](#5-mocking-a-property)
  - [6. More patching](#6-more-patching)
  - [7. Parameterize](#7-parameterize)
  - [8. Integration test: fixtures](#8-integration-test-fixtures)
- [How to Run](#how-to-run)
- [References](#references)

---

## Overview

This directory demonstrates best practices for writing Python unit and integration tests using `unittest`, `parameterized`, and `unittest.mock`. The focus is on:

- Parameterizing tests for concise coverage
- Mocking external dependencies (like HTTP requests)
- Patching methods and properties
- Integration testing with fixtures

---

## Tasks and Implementation

### 0. Parameterize a unit test

- **Goal:** Test `utils.access_nested_map` for various nested map structures and paths.
- **How:** Use `@parameterized.expand` to run the same test logic with different inputs and expected outputs.
- **Test file:** `test_utils.py`
- **Example:**
  ```python
  @parameterized.expand([
      ({"a": 1}, ("a",), 1),
      ({"a": {"b": 2}}, ("a",), {"b": 2}),
      ({"a": {"b": 2}}, ("a", "b"), 2),
  ])
  def test_access_nested_map(self, nested_map, path, expected):
      self.assertEqual(access_nested_map(nested_map, path), expected)
  ```

### 1. Parameterize a unit test (Exception)

- **Goal:** Ensure `utils.access_nested_map` raises `KeyError` for missing keys.
- **How:** Use `@parameterized.expand` and `assertRaises` context manager.
- **Test file:** `test_utils.py`
- **Example:**
  ```python
  @parameterized.expand([
      ({}, ("a",)),
      ({"a": 1}, ("a", "b")),
  ])
  def test_access_nested_map_exception(self, nested_map, path):
      with self.assertRaises(KeyError) as cm:
          access_nested_map(nested_map, path)
      self.assertEqual(str(cm.exception), repr(path[-1]))
  ```

### 2. Mock HTTP calls

- **Goal:** Test `utils.get_json` without making real HTTP requests.
- **How:** Patch `requests.get` to return a mock with a custom `.json()` method.
- **Test file:** `test_utils.py`
- **Example:**
  ```python
  @parameterized.expand([
      ("http://example.com", {"payload": True}),
      ("http://holberton.io", {"payload": False}),
  ])
  @patch('utils.requests.get')
  def test_get_json(self, test_url, test_payload, mock_get):
      mock_get.return_value.json.return_value = test_payload
      self.assertEqual(get_json(test_url), test_payload)
      mock_get.assert_called_once_with(test_url)
  ```

### 3. Parameterize and patch

- **Goal:** Test memoization using `utils.memoize` decorator.
- **How:** Patch the method being memoized and ensure it's called only once.
- **Test file:** `test_utils.py`
- **Example:**
  ```python
  class TestClass:
      def a_method(self):
          return 42
      @memoize
      def a_property(self):
          return self.a_method()
  with patch.object(TestClass, "a_method", return_value=42) as mock_method:
      obj = TestClass()
      self.assertEqual(obj.a_property, 42)
      self.assertEqual(obj.a_property, 42)
      mock_method.assert_called_once()
  ```

### 4. Parameterize and patch as decorators

- **Goal:** Test `client.GithubOrgClient.org` property.
- **How:** Use `@patch` to mock `get_json` and `@parameterized.expand` for different org names.
- **Test file:** `test_client.py`
- **Example:**
  ```python
  @parameterized.expand([
      ("google",),
      ("abc",),
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
      mock_get_json.return_value = {"login": org_name}
      client = GithubOrgClient(org_name)
      self.assertEqual(client.org, {"login": org_name})
      mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
  ```

### 5. Mocking a property

- **Goal:** Test `GithubOrgClient._public_repos_url` property.
- **How:** Patch `GithubOrgClient.org` to return a known payload and check the property.
- **Test file:** `test_client.py`
- **Example:**
  ```python
  with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
      mock_org.return_value = {"repos_url": "http://some_url"}
      client = GithubOrgClient("test")
      self.assertEqual(client._public_repos_url, "http://some_url")
  ```

### 6. More patching

- **Goal:** Test `GithubOrgClient.public_repos`.
- **How:** Patch both `get_json` and `_public_repos_url`.
- **Test file:** `test_client.py`
- **Example:**
  ```python
  @patch('client.get_json')
  def test_public_repos(self, mock_get_json):
      mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
      with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
          mock_url.return_value = "http://some_url"
          client = GithubOrgClient("test")
          self.assertEqual(client.public_repos(), ["repo1", "repo2"])
          mock_url.assert_called_once()
          mock_get_json.assert_called_once_with("http://some_url")
  ```

### 7. Parameterize

- **Goal:** Test `GithubOrgClient.has_license`.
- **How:** Parameterize with different repo and license key combinations.
- **Test file:** `test_client.py`
- **Example:**
  ```python
  @parameterized.expand([
      ({"license": {"key": "my_license"}}, "my_license", True),
      ({"license": {"key": "other_license"}}, "my_license", False),
  ])
  def test_has_license(self, repo, license_key, expected):
      self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
  ```

### 8. Integration test: fixtures

- **Goal:** Integration test for `GithubOrgClient.public_repos` using fixtures.
- **How:** Use `@parameterized_class` to inject fixtures, patch `requests.get` to return fixture payloads, and test integration logic.
- **Test file:** `test_client.py`
- **Example:**
  ```python
  @parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), FIXTURES)
  class TestIntegrationGithubOrgClient(unittest.TestCase):
      @classmethod
      def setUpClass(cls):
          cls.get_patcher = patch('requests.get')
          mock_get = cls.get_patcher.start()
          # Setup mock side_effect for .json() based on URL
      @classmethod
      def tearDownClass(cls):
          cls.get_patcher.stop()
      # Integration tests here
  ```

---

## How to Run

1. Install dependencies:
   ```bash
   pip install parameterized
   ```
2. Run the tests:
   ```bash
   python3 -m unittest test_utils.py
   python3 -m unittest test_client.py
   ```

---

## References

- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [parameterized](https://github.com/wolever/parameterized)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)
- [Python property mocking](https://docs.python.org/3/library/unittest.mock.html#mocking-properties)

---
