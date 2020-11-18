import psycopg2
import requests
import click

DATABASE_NAME = 'website_monitor'

def open_db():
	conn = None
	try:
		conn = psycopg2.connect(f'dbname={DATABASE_NAME}')
		return conn 
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	return False

def setup_db():
	stmt = open('setup.sql', 'r').read()
	try:
		conn = open_db()
		cur = conn.cursor()
		cur.execute(stmt)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def clean_db():
	conn = None
	stmt = (
		"""
			TRUNCATE data_points;
			TRUNCATE alerts;
		"""
	)
	try:
		conn = open_db()
		cur = conn.cursor()
		cur.execute(stmt)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def is_valid_url(url):
	try:
		requests.head(url)
	except Exception:
		return False
	return True

def check_uniqueness(sequence):
	return len(set(sequence)) == len(sequence)

def validate_websites(ctx, param, value):
	names = [name.lower() for name, _, _ in value]
	if not check_uniqueness(names):
		raise click.BadParameter('The names of websites should be unique.')
	
	urls = [url.lower() for _, url, _ in value]
	if not check_uniqueness(urls):
		raise click.BadParameter('The URLs should be unique.')
	
	for val in value:
		website, url, _ = val
		if not is_valid_url(url):
			raise click.BadParameter(f'{website}: the url provided ({url}) seems to be wrong. Please correct and try again.')
	return value
