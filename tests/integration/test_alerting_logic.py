import psycopg2
import concurrent.futures
from datetime import datetime
from unittest import mock
import requests_mock

from website_monitor.application import Application
from website_monitor.models.data_points import DataPointModel
from website_monitor.models.alerts import AlertModel
from website_monitor.utils import setup_db, clean_db

def test_alerting_logic(capsys):
  setup_db()
  
  # Options are formatted like Click provides them in the production environment.
  options = {
    # Two websites are monitored.
    'website': (
      ('test1', 'https://www.test1.com', 1),
      ('test2', 'https://www.test2.com', 1)
    ),
    'metrics': (
      (1, 1), # Metrics for the past minute are displayed every second.
      (10, 5) # Metrics for the past 10 minutes are displayed every 5 seconds.
    ),
    'period': 10, # Alerting period is 10 seconds.
    'threshold': 80 # Alerting threshold is 80.0%.
  }

  application = Application(
    options=options,
    data_points=DataPointModel(),
    alerts=AlertModel()
  )

  # Sentinel value is mocked to limit the number of iterations. We let the website monitors, metrics batches and the alerting system run for 10 iterations.
  with requests_mock.Mocker() as mock_requests, concurrent.futures.ThreadPoolExecutor() as executor:
    for website_monitor in application.websites_monitors:
      # The website test1 is down.
      mock_requests.get('https://www.test1.com', status_code=500)
      # The website test2 is up.
      mock_requests.get('https://www.test2.com', status_code=200)
      type(website_monitor).RUNNING = mock.PropertyMock(side_effect=range(10, -1, -1))
      executor.submit(website_monitor.start)

    for metrics_batch in application.metrics_batches:
      type(metrics_batch).RUNNING = mock.PropertyMock(side_effect=range(10, -1, -1))
      executor.submit(metrics_batch.start)

    type(application.alerting_system).RUNNING = mock.PropertyMock(side_effect=[1, 0])
    executor.submit(application.alerting_system.start)

  # We log the application data.
  type(application).RUNNING = mock.PropertyMock(side_effect=[1, 0])
  application.log()

  # We expect one alert to be created for website test1.
  alerts = application.alerts.all()
  assert len(alerts) == 1
  website, is_running, _, _, start_availability, end_availability = alerts[0]
  assert website == 'test1'
  assert is_running
  assert start_availability == 0.0
  assert end_availability == None

  actual_stout, _ = capsys.readouterr()
  expected = [
    'website_monitor - Website availability & performance monitoring',
    'test1',
    'test2',
    'Website',
    'Time',
    'Availability',
    'Maximum response time',
    'Average response time',
    'https://www.test1.com',
    'https://www.test2.com',
    'Availability alerts',
    'Metrics for the past 10min',
    'Metrics for the past 1min',
    'Threshold: 80% - Reference period: 10s',
    'Updates every 5s',
    'Updates every 1s',
  ]
  for string in expected:
    assert string in actual_stout

  clean_db()
