"""
Enums module for storing configuration values.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class DbConfig:
    HOST_NAME = os.getenv("DB_HOST_NAME", "")
    DATABASE = os.getenv("DB_DATABASE", "")
    USERNAME = os.getenv("DB_USERNAME", "")
    PWD = os.getenv("DB_PASSWORD", "")
    PORT_ID = os.getenv("DB_PORT_ID", "")

class WebConfig:
    INDEED_URL = "https://au.indeed.com/"

class JobConfig:
    JOB_TITLE = "python developer"
    LOCATION = "Sydney"
