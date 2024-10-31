import os
from numbers import Number

from flask import session
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

def sign_up_admin_user(data):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        # encrypt password using bcrypt

        cursor.execute(sql, (data['username'], data['password']))
        id = cursor.lastrowid
        conn.commit()
        print('회원가입 완료')

        return id

    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def sign_in_admin_user(data):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT u.id as users_id, u.username as username, s.id as stores_id, s.name as stores_name FROM users u, stores s WHERE u.id = s.users_id AND  username = %s AND password = %s'
        cursor.execute(sql, (data['username'], data['password']))
        result = cursor.fetchone()

        field = ['users_id', 'username', 'stores_id', 'stores_name']
        user = None

        if result:
            user = dict(zip(field, result))

        return user

    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()


def get_admin_user(username):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM admin_user WHERE username = %s'
        cursor.execute(sql, (username))
        users = cursor.fetchall()
        return users
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def create_store(data):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO stores (name, users_id) VALUES (%s, %s)'
        cursor.execute(sql, (data['name'], data['users_id']))
        id = cursor.lastrowid
        conn.commit()
        print('가게 생성 완료')
        return id
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()


def get_store_menu(store_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM stores_food WHERE store_id = %s'
        cursor.execute(sql, (store_id))
        menu = cursor.fetchall()
        return menu
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()
