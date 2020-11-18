from tabulate import tabulate
import pandas as pd

"""
Presenters are responsible for formatting the raw data as tables to display in the console.
"""
class OptionsPresenter:
	def __init__(self, options):
		self.options = options
	
	def format_data(self):
		data = []
		for opt in self.options:
			website, url, interval = opt
			data.append([website, url, f'Every {interval}s'])
		return data

	def to_table(self):
		data = self.format_data()
		return tabulate(
			data,
			headers=['Website', 'Url', 'Interval'],
			tablefmt='fancy_grid',
			showindex=False
		)

class MetricsPresenter:
	def __init__(self, metrics):
		self.metrics = metrics

	def to_table(self):
		data = pd.DataFrame(self.metrics, columns=['website', 'availability', 'max', 'avg'])
		data = data.round(3)
		data['availability'] = data['availability'].apply(lambda x: str(x) + '%')
		data['max'] = data['max'].apply(lambda x: str(x) + 's')
		data['avg'] = data['avg'].apply(lambda x: str(x) + 's')
		return tabulate(
			data,
			headers=['Website', 'Availability', 'Maximum response time', 'Average response time'],
			tablefmt='fancy_grid',
			showindex=False
		)

class AlertsPresenter:
	def __init__(self, alerts):
		self.alerts = alerts
	
	def format_data(self):
		data = []
		for alert in self.alerts:
			website, is_running, start_time, end_time, start_availability, end_availability = alert
			data.append(
				[website, start_time, f'Website {website} is down.', start_availability])
			if not is_running:
				data.append(
					[website, end_time, f'Website {website} is up.', end_availability])
		return data

	def to_table(self):
		data = self.format_data()
		data = pd.DataFrame(data, columns=['website', 'time', 'message', 'availability'])
		data.sort_values(by=['time'], inplace=True)
		data['availability'] = data['availability'].apply(lambda availability: str(availability) + '%')
		data['time'] = data['time'].apply(lambda time: time.strftime('%m/%d/%Y at %H:%M:%S'))
		return tabulate(
			data,
			headers=['Website', 'Time', 'Message', 'Availability'],
			tablefmt='fancy_grid',
			showindex=False
		)
