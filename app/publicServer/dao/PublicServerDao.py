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
