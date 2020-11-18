import psycopg2
from datetime import datetime, timedelta
from website_monitor.utils import open_db

class AlertModel:
	"""
	Data access layer for alerts.
	"""
	def insert(self, website, start_availability):
		conn = None
		stmt = (
			"""
				INSERT INTO alerts (website, start_time, start_availability)
				VALUES (%s, %s, %s)
				RETURNING id
			"""
		)
		alert_id = None
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (website, datetime.now(), start_availability))
			alert_id = cur.fetchone()[0]
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return alert_id

	def update(self, alert_id, is_running, end_time, end_availability):
		conn = None
		stmt = (
			"""
				UPDATE
					alerts
				SET
					is_running = %s,
					end_time = %s,
					end_availability = %s
				WHERE
					id = %s
			"""
		)
		updated_rows = 0
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (is_running, end_time, end_availability, alert_id))
			updated_rows = cur.rowcount
			conn.commit()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return updated_rows

	def get_running(self, website):
		conn = None
		stmt = (
			"""
				SELECT
					* 
				FROM
					alerts
				WHERE
					website = %s
				AND
					is_running = TRUE
				ORDER BY
					start_time DESC
				LIMIT
					1
			"""
		)
		row = None
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (website,))
			row = cur.fetchone()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return row
	
	def all(self):
		conn = None
		stmt = (
			"""
				SELECT
					website,
					is_running,
					start_time,
					end_time,
					start_availability,
					end_availability
				FROM
					alerts
				ORDER BY
					start_time DESC
			"""
		)
		rows = []
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt)
			rows = cur.fetchall()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return rows
