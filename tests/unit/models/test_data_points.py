import pytest
from unittest import mock
from website_monitor.models.data_points import DataPointModel

class TestDataPointModel:
  @pytest.fixture
  def data_point_model(self):
    return DataPointModel()

  @mock.patch('psycopg2.connect')
  def test_insert(self, mock_connect, data_point_model):
    expected = (1,)
    mock_connect.return_value.cursor.return_value.fetchone.return_value = expected
    actual = data_point_model.insert('test', 200, 1.17)
    assert actual == expected[0]
  
  @mock.patch('psycopg2.connect')
  def test_all_metrics(self, mock_connect, data_point_model):
    expected = (('test1', 100.0, 2.13, 1.12), ('test2', 98.0, 3.01, 0.77))
    mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
    actual = data_point_model.all_metrics(10)
    assert actual == expected
  
  @mock.patch('psycopg2.connect')
  def test_get_availabilities(self, mock_connect, data_point_model):
    expected = (('test1', 100.0), ('test2', 98.0))
    mock_connect.return_value.cursor.return_value.fetchall.return_value = expected
    actual = data_point_model.get_availabilities(10)
    assert actual == expected
  
  
