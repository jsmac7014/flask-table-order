import os
import pymysql
from flask.cli import load_dotenv

load_dotenv()

host = os.getenv("DATABASE_URL")
port = int(os.getenv("DATABASE_PORT"))
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = os.getenv("DATABASE_NAME")

def db_connect():
    try:
        print('연결 시도...')
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password, db=database, charset='utf8')

        print('연결 성공...')
        return conn
    except Exception as e:
        print('에러 발생', e)
        return None