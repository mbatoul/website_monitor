import pytest
from unittest import mock
from website_monitor.models.alerts import AlertModel
from datetime import datetime

class TestAlertModel:
  @pytest.fixture
  def alert_model(self):
    return AlertModel()

  @mock.patch('psycopg2.connect')
  def test_insert(self, mock_connect, alert_model):
    expected = (1,)
    mock_connect.return_value.cursor.return_value.fetchone.return_value = expected
    actual = alert_model.insert('test', 97.0)
    assert actual == expected[0]
  
  @mock.patch('psycopg2.connect')
  def test_update(self, mock_connect, alert_model):
    expected = 1
    mock_connect.return_value.cursor.return_value.rowcount = expected
    actual = alert_model.update(1, False, datetime(2020, 1, 1), 100.0)
    assert actual == expected

  @mock.patch('psycopg2.connect')
  def test_get_running(self, mock_connect, alert_model):
    expected = (1, 'test', True, datetime(2020, 1, 1), 78.0, None, None)
    mock_connect.return_value.cursor.return_value.fetchone.return_value = expected
    actual = alert_model.get_running('test')
    assert actual == expected
  
  @mock.patch('psycopg2.connect')
  def test_all(self, mock_connect, alert_model):
    expected = (
      ('test1', True, datetime(2020, 1, 1), 78.0, None, None),
      ('test2', False, datetime(2020, 1, 1), 87.0, datetime(2020, 1, 2), 100.0)
    )
    mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
    actual = alert_model.all()
    assert actual == expected
