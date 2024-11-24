from db.connect import db_connect

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

def get_stores_categories(store_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT DISTINCT category FROM stores_foods WHERE stores_id = %s'
        cursor.execute(sql, (store_id))
        result = cursor.fetchall()
        # print(result)
        field = ['name']
        categories = [dict(zip(field, r)) for r in result]
        print(categories)
        return categories
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def get_stores_foods(store_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT id, name, category, description, image_url, price FROM stores_foods WHERE stores_id = %s AND is_active = 1'
        cursor.execute(sql, (store_id))
        result = cursor.fetchall()
        field = ['id', 'name', 'category', 'description', 'image_url', 'price']
        menu = [dict(zip(field, m)) for m in result]

        return menu
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def get_stores_foods_detail(menu_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT id, name, category, description, image_url, price FROM stores_foods WHERE id = %s'
        cursor.execute(sql, (menu_id))
        result = cursor.fetchone()
        field = ['id', 'name', 'category', 'description', 'image_url', 'price']
        menu = dict(zip(field, result))

        return menu
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def create_store_foods(data):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'INSERT INTO stores_foods (name, category, description, image_url, price, stores_id) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (data['name'], data['category'], data['description'], data['image_url'], data['price'], data['stores_id']))
        conn.commit()
        print('메뉴 생성 완료')
        return True
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def soft_delete_stores_foods(data):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'UPDATE stores_foods SET is_active = 0 WHERE id = %s'
        cursor.execute(sql, (data['id']))
        conn.commit()
        print('메뉴 삭제 완료')
        return True
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()

def get_stores_foods_sales(stores_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
            SELECT f.name, SUM(ohf.quantity) as quantity, SUM(ohf.quantity * f.price) as sales
            FROM orders_has_foods ohf, stores_foods f, orders o
            WHERE ohf.stores_foods_id = f.id AND ohf.orders_id = o.id AND f.stores_id = %s AND o.status = 'CONFIRM'
            GROUP BY f.name
        """
        cursor.execute(sql, (stores_id))
        result = cursor.fetchall()

        return result
    except Exception as e:
        print('에러 발생', e)
        return None
    finally:
        conn.close()