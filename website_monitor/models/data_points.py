import psycopg2
from datetime import datetime, timedelta
from website_monitor.utils import open_db

class DataPointModel:
	"""
	Data access layer for data points.
	"""
	def insert(self, website, response_code, response_time):
		conn = None
		stmt = (
			"""
				INSERT INTO data_points (website, response_code, response_time)
				VALUES (%s, %s, %s)
				RETURNING id
			"""
		)
		data_point_id = None
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (website, response_code, response_time))
			conn.commit()
			data_point_id = cur.fetchone()[0]
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return data_point_id

	def all_metrics(self, period_in_minutes):
		conn = None
		start_time = datetime.now() - timedelta(minutes=period_in_minutes)
		stmt = (
			"""
				SELECT 
					DISTINCT(website) as website,
					ROUND(100.0 * SUM(CASE WHEN response_code = 200 THEN 1 ELSE 0 END) / COUNT(id), 1) as availability,
					MAX(response_time) as max,
					AVG(response_time) as avg
				FROM
					data_points
				WHERE
					time >= %s
				GROUP BY
					website
				ORDER BY
					website ASC
			"""
		)
		rows = []
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (start_time,))
			rows = cur.fetchall()
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return rows

	def get_availabilities(self, period_in_seconds):
		conn = None
		start_time = datetime.now() - timedelta(seconds=period_in_seconds)
		stmt = (
			"""
				SELECT
					DISTINCT(website) as website,
					ROUND(100.0 * SUM(CASE WHEN response_code = 200 THEN 1 ELSE 0 END) / COUNT(id), 1) as availability
				FROM
					data_points
				WHERE
					time >= %s
				GROUP BY
					website
				ORDER BY
					website ASC
			"""
		)
		rows = []
		try:
			conn = open_db()
			cur = conn.cursor()
			cur.execute(stmt, (start_time,))
			rows = cur.fetchall()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
		return rows
