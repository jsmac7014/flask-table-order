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

def get_store_categories(store_id):
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

def get_store_menu(store_id):
    conn = db_connect()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = 'SELECT id, name, category, description, image_url, price FROM stores_foods WHERE stores_id = %s'
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