"""
The main entry point. Invoke as `website_monitor' or `python website_monitor'.
"""
import click

from website_monitor.utils import setup_db, clean_db, validate_websites
from website_monitor.application import Application
from website_monitor.models.data_points import DataPointModel
from website_monitor.models.alerts import AlertModel

@click.command()
@click.option('--website', '--w', type=(str, str, click.IntRange(min=1)), callback=validate_websites, multiple=True, required=True, help='Name, URL and check interval in seconds (min 1s) for a website. Example: --website github https://www.github.com 1 --website reddit https://www.reddit.com 1')
@click.option('--metrics', '--m', type=(int, int), multiple=True, default=((10, 10), (60, 60)), show_default=True, help='Reference period and refresh interval for a set of the tracked metrics. Example: --metrics 120 30 <=> Metrics for past 120 minutes should be refreshed every 30 seconds.')
@click.option('--period', '--p', type=int, default=120, show_default=True, help='Alerting period in seconds. Combined with alerting threshold. Example: --period 180 <=> Websites\' availabilities over the last 3 minutes will be considered to open/close alerts.')
@click.option('--threshold', '--t', type=click.IntRange(min=1, max=99), default=80, show_default=True, help="Alerting threshold in %. Must be between 1% and 99%. Combined with alerting period. Example: --threshold 90 <=> When a website availability is below (resp. above) 90% during the period of reference, an alert is opened (resp. closed).")
def main(website, metrics, period, threshold):
	setup_db()
	application = Application(
		options=locals(),
		data_points=DataPointModel(),
		alerts=AlertModel()
	)
	try:
		application.run()
	except KeyboardInterrupt as error:
		click.echo(error)
	finally:
		clean_db()

if __name__ == '__main__':
	main()
