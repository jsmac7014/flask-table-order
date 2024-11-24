from dataclasses import field

from db.connect import db_connect

def create_stores_tables(data):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO stores_tables (name, min_seat, max_seat, stores_id) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (data['name'], data['min_seat'], data['max_seat'], data['stores_id']))
        id = cursor.lastrowid
        conn.commit()

        return id
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()



def get_stores_tables(store_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'SELECT id, name, min_seat, max_seat FROM stores_tables WHERE stores_id = %s'
        cursor.execute(sql, (store_id))
        result = cursor.fetchall()

        field = ['id', 'name', 'min_seat', 'max_seat']
        tables = [dict(zip(field, r)) for r in result]

        return tables
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()



    return None

def get_stores_tables_detail(table_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = """SELECT name, min_seat, max_seat, order_date, status, quantity, stores_foods_id FROM stores_tables t
                LEFT JOIN orders o ON o.stores_tables_id = t.id
                LEFT JOIN orders_has_foods ohf ON ohf.orders_id = o.id
                WHERE t.id = %s
                """
        cursor.execute(sql, (table_id))
        result = cursor.fetchall()

        field = ['name', 'min_seat', 'max_seat', 'order_date', 'status', 'quantity', 'stores_foods_id']
        table = dict(zip(field, result))

        return table
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

    return None

def get_stores_tables_orders(table_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'SELECT id, order_date, status FROM orders WHERE stores_tables_id = %s'
        cursor.execute(sql, (table_id))
        result = cursor.fetchall()

        field = ['id', 'order_date', 'status']
        orders = [dict(zip(field, r)) for r in result]

        return orders
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()


def get_stores_tables_name(table_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'SELECT name FROM stores_tables WHERE id = %s'
        cursor.execute(sql, (table_id))
        result = cursor.fetchone()

        return result[0]
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

    return None
