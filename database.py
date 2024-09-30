"""
Database module for managing the storage of scraped job data into PostgreSQL.
"""

import psycopg2
from loguru import logger
from enums import DbConfig
from dotenv import load_dotenv

load_dotenv()
class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_db_connection(self):
        """
        Establish and return a database connection.
        """
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST_NAME"),
            dbname=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT_ID")
        )
        return self.conn

    def create_jobs_table(self):
        """
        Create the JobsData table in PostgreSQL.
        """
        try:
            self.get_db_connection()
            self.cur = self.conn.cursor()
            self.cur.execute("DROP TABLE IF EXISTS JobsData")

            create = """
            CREATE TABLE IF NOT EXISTS JobsData (
                id serial PRIMARY KEY NOT NULL,
                job_title VARCHAR(255),
                company_name VARCHAR(255),
                location VARCHAR(255)
            );
            """
            self.cur.execute(create)
            self.conn.commit()
            logger.info("JobsData table created successfully.")
        except Exception as error:
            logger.error(error)
        finally:
            if self.cur is not None:
                self.cur.close()
            if self.conn is not None:
                self.conn.close()

    def store_data(self, jobs_list, company_list, location_list):
        """
        Store the scraped data in PostgreSQL.
        """
        try:
            self.get_db_connection()
            self.cur = self.conn.cursor()

            insert_script = 'INSERT INTO JobsData (job_title, company_name, location) VALUES (%s, %s, %s)'
            insert_values = list(zip(jobs_list, company_list, location_list))
            self.cur.executemany(insert_script, insert_values)

            self.conn.commit()
            logger.info("Data scraped and stored successfully.")
        except Exception as error:
            logger.error(error)
        finally:
            if self.cur is not None:
                self.cur.close()
            if self.conn is not None:
                self.conn.close()
