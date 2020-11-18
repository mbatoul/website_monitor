import pytest
import requests_mock
from unittest import mock
from datetime import datetime

from website_monitor.core import WebsiteMonitor, MetricsBatch, AlertingSystem
from website_monitor.models.data_points import DataPointModel
from website_monitor.models.alerts import AlertModel

class TestWebsiteMonitor:
  @pytest.fixture
  def website_monitor(self):
    website_monitor = WebsiteMonitor(
      'test',
      'https://www.test.com',
      5,
      None
    )
    return website_monitor
  
  def test_check(self, website_monitor):
    with requests_mock.Mocker() as mock:
      mock.get('https://www.test.com', status_code=200)
      actual_resp_code, actual_resp_time = website_monitor.check()
    assert actual_resp_code == 200
    assert actual_resp_time == pytest.approx(0.0, abs=1)
    
    with requests_mock.Mocker() as mock:
      mock.get('https://www.test.com', status_code=500)
      actual_resp_code, actual_resp_time = website_monitor.check()
    assert actual_resp_code == 500
    assert actual_resp_time == pytest.approx(0.0, abs=1)


class TestMetricsBatch:
  @pytest.fixture
  def metrics_batch(self):
    metrics_batch = MetricsBatch(
      10,
      5,
      DataPointModel()
    )
    return metrics_batch
  
  @mock.patch('psycopg2.connect')
  def test_refresh(self, mock_connect, metrics_batch):
    expected = (('test1', 100.0, 2.13, 1.12), ('test2', 98.0, 3.01, 0.77))
    mock_connect.return_value.cursor.return_value.fetchall.return_value = expected

    now = datetime.now()
    metrics_batch.refresh()
    
    actual = metrics_batch.metrics
    assert expected == actual

    actual = metrics_batch.last_update_time
    diff = (actual - now).total_seconds()
    assert diff == pytest.approx(0.0, abs=1)
  
class TestAlertingSystem:
  @pytest.fixture
  def alerting_system(self):
    alerting_system = AlertingSystem(
      2,
      80.0,
      DataPointModel(),
      AlertModel()
    )
    return alerting_system
  
  def test_should_open_alert(self, alerting_system):
    # Website up and no running alert
    assert not alerting_system.should_open_alert(90.0, None)
    # Website up and running alert
    assert not alerting_system.should_open_alert(90.0, DummyAlert())
    # Website down and no running alert
    assert alerting_system.should_open_alert(60.0, None)
    # Website down and running alert
    assert not alerting_system.should_open_alert(60.0, DummyAlert())

  
  def test_should_close_alert(self, alerting_system):
    # Website up and no running alert
    assert not alerting_system.should_close_alert(90.0, None)
    # Website up and running alert
    assert alerting_system.should_close_alert(90.0, DummyAlert())
    # Website down and no running alert
    assert not alerting_system.should_close_alert(60.0, None)
    # Website down and running alert
    assert not alerting_system.should_close_alert(60.0, DummyAlert())
  
  def test_open_alert(self, alerting_system):
    model = alerting_system.alerts
    model.insert = mock.MagicMock()
    alerting_system.open_alert('test', 75.0)
    model.insert.assert_called_with('test', 75.0)
  
  def test_close_alert(self, alerting_system):
    model = alerting_system.alerts
    model.update = mock.MagicMock()
    alerting_system.close_alert(1, 90.0)
    model.update.assert_called()
  
  @mock.patch('psycopg2.connect')
  def test_check_availability(self, mock_connect, alerting_system):
    website = 'test'
    
    # Website is up and there is no running alert => no alert opened or closed
    alerting_system.open_alert, alerting_system.close_alert = mock.MagicMock(), mock.MagicMock()
    availability, running_alert = 90.0, None
    mock_connect.return_value.cursor.return_value.fetchone.return_value = running_alert
    alerting_system.check_availability(website, availability)
    assert not alerting_system.open_alert.called
    assert not alerting_system.close_alert.called
    
    # Website is up and there is a running alert => the running alert is closed
    alerting_system.open_alert, alerting_system.close_alert = mock.MagicMock(), mock.MagicMock()
    availability, running_alert = 90.0, (1, website, True, datetime(2020, 1, 1), 78.0, None, None)
    mock_connect.return_value.cursor.return_value.fetchone.return_value = running_alert
    alerting_system.check_availability(website, availability)
    assert not alerting_system.open_alert.called
    assert alerting_system.close_alert.called

    # Website is down and there is no running alert => an alert is opened
    alerting_system.open_alert, alerting_system.close_alert = mock.MagicMock(), mock.MagicMock()
    availability, running_alert = 75.0, None
    mock_connect.return_value.cursor.return_value.fetchone.return_value = running_alert
    alerting_system.check_availability(website, availability)
    assert alerting_system.open_alert.called
    assert not alerting_system.close_alert.called

    # Website is down and there is a running alert => no alert opened or closed
    alerting_system.open_alert, alerting_system.close_alert = mock.MagicMock(), mock.MagicMock()
    availability, running_alert = 75.0, (1, website, True, datetime(2020, 1, 1), 78.0, None, None)
    mock_connect.return_value.cursor.return_value.fetchone.return_value = running_alert
    alerting_system.check_availability(website, availability)
    assert not alerting_system.open_alert.called
    assert not alerting_system.close_alert.called

  @mock.patch('psycopg2.connect')
  def test_check_availabilities(self, mock_connect, alerting_system):
    availabilities = (('test1', 100.0), ('test2', 98.0))
    mock_connect.return_value.cursor.return_value.fetchall.return_value = availabilities
    alerting_system.check_availabilities = mock.MagicMock()
    alerting_system.check_availabilities()
    assert alerting_system.check_availabilities.called

class DummyAlert:
  def __init__(self):
    pass
