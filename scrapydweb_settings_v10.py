import os

SCRAPYDWEB_PORT = 55000
ENABLE_AUTH = True
USERNAME = "admin"
PASSWORD = os.environ.get("PASSWORD", "admin")
SCRAPYD_SERVERS = [
    "127.0.0.1:6800",
]
LOCAL_SCRAPYD_SERVER = "127.0.0.1:6800"
LOCAL_SCRAPYD_LOGS_DIR = "logs"
ENABLE_LOGPARSER = True
SCHEDULE_CUSTOM_USER_AGENT = "Mozilla/5.0"
SCHEDULE_ADDITIONAL = "-d setting=CLOSESPIDER_TIMEOUT=60\r\n-d setting=CLOSESPIDER_PAGECOUNT=10\r\n-d arg1=val1"
ENABLE_MONITOR = True
ALERT_WORKING_DAYS = [1, 2, 3, 4, 5, 6, 7]
ALERT_WORKING_HOURS = [9]
DATA_PATH = os.environ.get("DATA_PATH", "./database")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./database")
