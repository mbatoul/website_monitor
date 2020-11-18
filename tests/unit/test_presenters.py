import pytest
from website_monitor.presenters import OptionsPresenter, MetricsPresenter, AlertsPresenter
from datetime import datetime, timedelta

class TestOptionsPresenter:
	@pytest.fixture
	def options_presenter(self):
		options = (
			('test1', 'https://www.test1.com', 1),
			('test2', 'https://www.test2.com', 2)
		)
		return OptionsPresenter(options)

	def test_format_data(self, options_presenter):
		expected = [
			['test1', 'https://www.test1.com', 'Every 1s'],
			['test2', 'https://www.test2.com', 'Every 2s']
		]
		actual = options_presenter.format_data()
		assert expected == actual
	
	def test_to_table(self, options_presenter):
		expected = '\n'.join(
				[
					'╒═══════════╤═══════════════════════╤════════════╕',
					'│ Website   │ Url                   │ Interval   │',
					'╞═══════════╪═══════════════════════╪════════════╡',
					'│ test1     │ https://www.test1.com │ Every 1s   │',
					'├───────────┼───────────────────────┼────────────┤',
					'│ test2     │ https://www.test2.com │ Every 2s   │',
					'╘═══════════╧═══════════════════════╧════════════╛',
				]
		)
		actual = options_presenter.to_table()
		assert expected == actual

class TestMetricsPresenter:
	@pytest.fixture
	def metrics_presenter(self):
		metrics = [
			('test1', 100.0, 1.17, 0.07),
			('test2', 87.1, 2.87, 0.31),
		]
		return MetricsPresenter(metrics)

	def test_to_table(self, metrics_presenter):
		expected = '\n'.join(
				[
					'╒═══════════╤════════════════╤═════════════════════════╤═════════════════════════╕',
					'│ Website   │ Availability   │ Maximum response time   │ Average response time   │',
					'╞═══════════╪════════════════╪═════════════════════════╪═════════════════════════╡',
					'│ test1     │ 100.0%         │ 1.17s                   │ 0.07s                   │',
					'├───────────┼────────────────┼─────────────────────────┼─────────────────────────┤',
					'│ test2     │ 87.1%          │ 2.87s                   │ 0.31s                   │',
					'╘═══════════╧════════════════╧═════════════════════════╧═════════════════════════╛',
				]
		)
		actual = metrics_presenter.to_table()
		assert expected == actual

class TestAlertsPresenter:
	@pytest.fixture
	def alerts_presenter(self):
		alerts = (
			('test1', True, datetime(2020, 1, 1), None, 79.0, None),
			('test2', False, datetime(2020, 1, 1), datetime(2020, 1, 2), 67.0, 100.0),
		)
		return AlertsPresenter(alerts)

	def test_format_data(self, alerts_presenter):
		expected = [
			['test1', datetime(2020, 1, 1, 0, 0), 'Website test1 is down.', 79.0],
			['test2', datetime(2020, 1, 1, 0, 0), 'Website test2 is down.', 67.0],
			['test2', datetime(2020, 1, 2, 0, 0), 'Website test2 is up.', 100.0]
		]
		actual = alerts_presenter.format_data()
		assert expected == actual
	
	def test_to_table(self, alerts_presenter):
		expected = '\n'.join(
			[
				'╒═══════════╤════════════════════════╤════════════════════════╤════════════════╕',
				'│ Website   │ Time                   │ Message                │ Availability   │',
				'╞═══════════╪════════════════════════╪════════════════════════╪════════════════╡',
				'│ test1     │ 01/01/2020 at 00:00:00 │ Website test1 is down. │ 79.0%          │',
				'├───────────┼────────────────────────┼────────────────────────┼────────────────┤',
				'│ test2     │ 01/01/2020 at 00:00:00 │ Website test2 is down. │ 67.0%          │',
				'├───────────┼────────────────────────┼────────────────────────┼────────────────┤',
				'│ test2     │ 01/02/2020 at 00:00:00 │ Website test2 is up.   │ 100.0%         │',
				'╘═══════════╧════════════════════════╧════════════════════════╧════════════════╛',
			]
		)
		actual = alerts_presenter.to_table()
		assert expected == actual
