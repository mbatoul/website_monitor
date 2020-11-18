import requests
import time
from datetime import datetime
from website_monitor.loop_runner import LoopRunner
class WebsiteMonitor(LoopRunner):
	"""
	Pings a given website at given interval and saves response codes and times to database.
	"""
	def __init__(self, website, url, check_interval, data_points):
		self.website = website
		self.url = url
		self.check_interval = check_interval
		self.data_points = data_points

	def check(self):
		start = datetime.now()
		response = requests.get(self.url)
		response_time = (datetime.now() - start).total_seconds()
		return response.status_code, response_time
	
	def save_data_point(self, response_code, response_time):
		self.data_points.insert(self.website, response_code, response_time)

	def start(self):
		while self.RUNNING:
			response_code, response_time = self.check()
			self.save_data_point(response_code, response_time)
			time.sleep(self.check_interval)

class MetricsBatch(LoopRunner):
	"""
	Extract metrics from database at a given interval and store them to be displayed.
	"""
	def __init__(self, period, interval, data_points):
		self.period = period
		self.interval = interval
		self.data_points = data_points
		self.last_update_time = datetime.now()
		self.metrics = None

	def refresh(self):
		self.metrics = self.data_points.all_metrics(self.period)
		self.last_update_time = datetime.now()

	def start(self):
		while self.RUNNING:
			self.refresh()
			time.sleep(self.interval)

class AlertingSystem(LoopRunner):
	"""
	Extracts websites' availabilities at a given interval and opens/closes alerts.
	An alert is opened (resp. closed) when availability is below (resp. above) the given threshold for the given period.
	"""
	def __init__(self, period, threshold, data_points, alerts):
		self.period = period
		self.threshold = threshold
		self.data_points = data_points
		self.alerts = alerts

	def should_open_alert(self, availability, running_alert):
		return availability < self.threshold and running_alert is None
	
	def should_close_alert(self, availability, running_alert):
		return availability >= self.threshold and running_alert is not None
	
	def open_alert(self, website, availability):
		self.alerts.insert(website, availability)
	
	def close_alert(self, alert_id, availability):
		self.alerts.update(alert_id, False, datetime.now(), availability)
	
	def check_availability(self, website, availability):
		running_alert = self.alerts.get_running(website)
		if self.should_open_alert(availability, running_alert):
			self.open_alert(website, availability)
		elif self.should_close_alert(availability, running_alert):
			alert_id = running_alert[0]
			self.close_alert(alert_id, availability)
	
	def check_availabilities(self):
		availabilities = self.data_points.get_availabilities(self.period)
		for website, availability in availabilities:
			self.check_availability(website, availability)

	def start(self):
		time.sleep(self.period)
		while self.RUNNING:
			self.check_availabilities()
			time.sleep(1)
