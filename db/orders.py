from db.connect import db_connect

def create_order(data):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO orders (order_date, status, stores_tables_id) VALUES (%s, %s, %s)'
        cursor.execute(sql, (data['order_date'], data['status'], data['stores_tables_id']))
        id = cursor.lastrowid
        conn.commit()
        return id
    except Exception as e:
        print('에러 발생', e)
        conn.rollback()
        return None
    finally:
        conn.close()

def create_orders_has_foods(orders, orders_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO orders_has_foods (quantity, orders_id, stores_foods_id) VALUES (%s, %s, %s)'

        rows = [(data['quantity'], orders_id, data['stores_foods_id']) for data in orders]
        cursor.executemany(sql, rows)
        conn.commit()
        return True
    except Exception as e:
        print('에러 발생', e)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_last_orders_id(stores_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = """
                SELECT o.id FROM orders o, stores_tables t
                WHERE o.stores_tables_id = t.id AND t.stores_id = %s
                ORDER BY o.id DESC LIMIT 1
        """
        cursor.execute(sql, (stores_id))
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def get_new_orders(stores_id, last_orders_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = """
                SELECT o.id FROM orders o, stores_tables t
                WHERE o.stores_tables_id = t.id AND t.stores_id = %s AND o.id > %s 
                ORDER BY o.id ASC
        """
        cursor.execute(sql, (stores_id, last_orders_id))
        result = cursor.fetchall()
        field = ['id']
        result = [dict(zip(field, r)) for r in result]
        return result
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def get_orders_list(store_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = """
            SELECT orders_id, t.id, t.name, status, o.order_date FROM orders_has_foods ohf, orders o, stores_tables t
            WHERE ohf.orders_id = o.id AND o.stores_tables_id = t.id AND t.stores_id = %s
            GROUP BY orders_id
        """

        cursor.execute(sql, (store_id))
        result = cursor.fetchall()
        field = ['orders_id', 'stores_tables_id', 'table_name', 'status', 'order_date']
        orders = [dict(zip(field, r)) for r in result]

        return orders
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()