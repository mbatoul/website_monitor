import time
from datetime import datetime
import concurrent.futures
import click

from website_monitor.core import WebsiteMonitor, AlertingSystem, MetricsBatch
from website_monitor.presenters import OptionsPresenter, AlertsPresenter, MetricsPresenter
from website_monitor.loop_runner import LoopRunner

class Application(LoopRunner):
	"""
	The main class of the program. Responsible for parsing options and launching the main features in different threads.
	"""
	def __init__(self, options, data_points, alerts):
		self.options = options
		self.data_points = data_points
		self.alerts = alerts
		self.start_time = datetime.now()
		self.metrics_batches = [
			MetricsBatch(*opts, self.data_points) for opts in set(self.options['metrics'])
		]
		self.alerting_system = AlertingSystem(
			self.options['period'],
			self.options['threshold'],
			self.data_points,
			self.alerts
		)
		self.websites_monitors = [
			WebsiteMonitor(*opts, self.data_points) for opts in self.options['website']
		]

	def log(self):
		"""
		Displays data to user in the console.
		"""
		while self.RUNNING:
			click.clear()

			click.secho('website_monitor - Website availability & performance monitoring', fg='blue', bold=True)
			click.echo(f"Started on {self.start_time.strftime('%m/%d/%Y at %H:%M:%S')}")
			options = self.options['website']
			options_table = OptionsPresenter(options).to_table()
			click.echo(options_table)
			click.echo('\n')

			click.secho('Availability alerts', fg='red', bold=True)
			alerts = self.alerts.all()
			alerts_table = AlertsPresenter(alerts).to_table()
			click.echo(alerts_table)
			click.echo(f'Threshold: {self.alerting_system.threshold}% - Reference period: {self.alerting_system.period}s')
			click.echo('\n')

			for metrics_batch in self.metrics_batches:
				click.secho(f'Metrics for the past {metrics_batch.period}min', fg='cyan', bold=True)
				metrics = metrics_batch.metrics
				metrics_table = MetricsPresenter(metrics).to_table()
				click.echo(metrics_table)
				click.secho(f"Last update: {metrics_batch.last_update_time.strftime('%H:%M:%S')} - Updates every {metrics_batch.interval}s")
				click.echo('\n')

			time.sleep(1)

	def run(self):
		"""
		Runs the main features on different threads.
		"""
		with concurrent.futures.ThreadPoolExecutor() as executor:
			# Runs the websites monitors
			for monitor in self.websites_monitors:
				executor.submit(monitor.start)
			# Runs the metrics batches
			for metrics_batch in self.metrics_batches:
				executor.submit(metrics_batch.start)
			# Runs the alerting system
			executor.submit(self.alerting_system.start)
			# Logs monitoring data
			executor.submit(self.log)

