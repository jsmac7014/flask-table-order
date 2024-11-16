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
        cursor.close()
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
        cursor.close()
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
            ORDER BY orders_id DESC
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
        cursor.close()
        conn.close()

def get_orders_detail(orders_id, stores_id):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = """
            SELECT f.name, ohf.quantity, f.price FROM orders_has_foods ohf, stores_foods f
            WHERE ohf.stores_foods_id = f.id AND ohf.orders_id = %s AND f.stores_id = %s
        """

        cursor.execute(sql, (orders_id, stores_id))
        result = cursor.fetchall()
        field = ['name', 'quantity', 'price']
        orders = [dict(zip(field, r)) for r in result]

        return orders
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        cursor.close()
        conn.close

def update_order_status(data):
    conn = db_connect()

    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        sql = 'UPDATE orders SET status = %s WHERE id = %s'
        cursor.execute(sql, (data['status'], data['orders_id']))
        conn.commit()
        return True
    except Exception as e:
        print('에러 발생', e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()