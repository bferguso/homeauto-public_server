import psycopg2
import psycopg2.extras
import os


class PublicServerDao:
    def __init__(self):
        pass

    user = os.getenv("DB_SCHEMA")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")

    def get_connection(self):
        return psycopg2.connect("dbname="+self.database+" user="+self.user+" password="+self.password)

    def get_cursor(self, connection):
        cur = connection.cursor()
        cur.execute("SET search_path TO " + self.user)
        return cur

    def log_access(self, env_data):
        conn = self.get_connection()
        cur = self.get_cursor(conn)
        cur.execute("insert into ps_access_log (access_url, access_ip, access_timestamp ) values( %s, %s, current_timestamp );"
                    , (env_data['url'], env_data['remote_address']))
        conn.commit()
        cur.close()
        conn.close()

    def get_visitor_info(self):
        conn = self.get_connection()
        cur = self.get_cursor(conn)
        cur.execute("select count(*) from ps_access_log;")
        visitor_count = cur.fetchone()
        cur.execute("select min(access_timestamp) from ps_access_log;")
        first_visitor = cur.fetchone()
        cur.close()
        conn.close()
        return {"visitors": visitor_count[0], "since": first_visitor[0]}
