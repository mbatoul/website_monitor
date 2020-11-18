import pytest
import requests_mock
from website_monitor.utils import check_uniqueness, is_valid_url, open_db

def test_check_uniqueness():
  assert check_uniqueness([1, 2, 3])
  assert not check_uniqueness([1, 2, 2])

def test_is_valid_url():
  with requests_mock.Mocker() as mock:
    mock.head('https://www.test1.com', status_code=200)
    assert is_valid_url('https://www.test1.com')

  assert not is_valid_url('https://www.test2.com')
