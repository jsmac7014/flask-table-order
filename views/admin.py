from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from werkzeug.utils import secure_filename

from db.auth import sign_in_admin_user, sign_up_admin_user, check_admin_user_with_stores_id
from db.orders import get_orders_list, get_orders_detail, update_order_status, get_all_orders_with_detail
from db.stores import create_store, get_stores_foods, create_store_foods, get_stores_foods_detail, \
    soft_delete_stores_foods, get_stores_foods_sales
from db.stores_tables import get_stores_tables, create_stores_tables, get_stores_tables_detail, get_stores_tables_orders
import csv
from s3_connect import upload_file

admin = Blueprint('admin', __name__)


def is_logged_in():
    return session.get('logged_in')



@admin.route('/table')
def table():
    tables = get_stores_tables(session['stores_id'])
    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/table/table.html', tables=tables)


@admin.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if is_logged_in():
        return redirect('/admin/table')

    if request.method == 'GET':
        return render_template('admin/auth/sign-in.html')

    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = sign_in_admin_user({'username': username, 'password': password})
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['stores_id'] = user['stores_id']
            session['stores_name'] = user['stores_name']
            return redirect('/admin/table')
        else:
            return '로그인 실패'


@admin.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if is_logged_in():
        return redirect('/admin')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        store_name = request.form.get('store_name')

        users_id = sign_up_admin_user({'username': username, 'password': password})
        stores_id = create_store({'name': store_name, 'users_id': users_id})

        session['email'] = username
        session['stores_id'] = stores_id
        session['logged_in'] = True

        return redirect('/admin/table')
    return render_template('admin/auth/sign-up.html')


@admin.route('/sign-out')
def sign_out():
    session.clear()
    return redirect('/admin/sign-in')


@admin.route('/check/auth', methods=['POST'])
def check_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    stores_id = data['stores_id']

    result = check_admin_user_with_stores_id({'username': username, 'password': password, 'stores_id': stores_id})
    # print(result)
    if result:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


@admin.route('/menu/upload', methods=['POST'])
def upload():
    if not is_logged_in():
        return redirect('/admin/sign-in')

    file = request.files['image']
    filename = secure_filename(file.filename)

    url = upload_file(file, filename)
    return url
    # return redirect('/admin')


@admin.route('/menu')
def menu():
    menus = get_stores_foods(session['stores_id'])

    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/menu/menu.html', menus=menus)


# menu detail route
@admin.route('/menu/<menu_id>/edit', methods=['GET'])
def menu_edit(menu_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')
    detail = get_stores_foods_detail(menu_id)
    print(detail)
    return render_template('admin/menu/menu-edit.html', detail=detail, menu_id=menu_id)

@admin.route('/menu/<menu_id>/update', methods=['POST'])
def menu_update(menu_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')
    data = {
        'id': menu_id,
        'name': request.form.get('name'),
        'description': request.form.get('description'),
    }
    # create_store_foods(data)
    return redirect('/admin/menu')
@admin.route('/menu/create', methods=['POST'])
def menu_create():
    if not is_logged_in():
        return redirect('/admin/sign-in')
    data = {
        'name': request.form.get('name'),
        'category': request.form.get('category'),
        'description': request.form.get('description'),
        'image_url': request.form.get('image_url'),
        'price': request.form.get('price'),
        'stores_id': session['stores_id']
    }
    create_store_foods(data)
    return redirect('/admin/menu')

@admin.route('/menu/<menu_id>/delete', methods=['POST'])
def menu_delete(menu_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = {
        'id': menu_id
    }
    result = soft_delete_stores_foods(data)
    return redirect('/admin/menu')

@admin.route('/order')
def order():
    if not is_logged_in():
        return redirect('/admin/sign-in')
    stores_id = session['stores_id']
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'ALL')

    if page < 1:
        page = 1
    orders_list = get_orders_list(stores_id, page, status)

    return render_template('admin/order/order.html', orders=orders_list, page = page, status = status)

@admin.route('/order/detail/<order_id>', methods=['POST'])
def order_detail(order_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = request.get_json()

    orders_id = data['orders_id']
    stores_id = session['stores_id']

    orders = get_orders_detail(orders_id, stores_id)
    return jsonify(orders)

@admin.route('/order/confirm/<order_id>', methods=['POST'])
def order_confirm(order_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = request.get_json()
    orders_id = data['orders_id']

    result = update_order_status({'orders_id': orders_id, 'status': 'CONFIRM'})

    return jsonify({'status': 'success'})

@admin.route('/order/cancel/<order_id>', methods=['POST'])
def order_cancel(order_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = request.get_json()
    orders_id = data['orders_id']

    result = update_order_status({'orders_id': orders_id, 'status': 'CANCEL'})

    return jsonify({'status': 'success'})

@admin.route('/table/create', methods=['POST'])
def table_create():
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = {
        'name': request.form.get('name'),
        'min_seat': request.form.get('min_seat'),
        'max_seat': request.form.get('max_seat'),
        'stores_id': session['stores_id']
    }

    create_stores_tables(data)

    return redirect('/admin/table')


@admin.route('/table/<table_id>/detail', methods=['GET'])
def table_detail(table_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')
    table = get_stores_tables_detail(table_id)
    orders = get_stores_tables_orders(table_id)
    return render_template('admin/table/table-detail.html', table=table, orders=orders)


@admin.route('/order/csv/download', methods=['GET'])
def csv_download():
    if not is_logged_in():
        return redirect('/admin/sign-in')

    stores_id = session['stores_id']

    csv_data = '주문 ID,주문 날짜,상태,테이블 이름,메뉴 이름,수량,가격\n'
    orders = get_all_orders_with_detail(stores_id)
    # create dummy data for testing
    for order in orders:
        csv_data += ','.join(map(str, order)) + '\n'

    with open('orders.csv', 'w', encoding='utf-8-sig') as f:
        f.write(csv_data)

    return send_file('orders.csv', as_attachment=True)

@admin.route('/menu/csv/download', methods=['GET'])
def csv_download_menu():
    if not is_logged_in():
        return redirect('/admin/sign-in')

    stores_id = session['stores_id']

    csv_data = '메뉴 이름,수량,매출\n'
    menus = get_stores_foods_sales(stores_id)
    # create dummy data for testing
    for menu in menus:
        csv_data += ','.join(map(str, menu)) + '\n'

    with open('menus.csv', 'w', encoding='utf-8-sig') as f:
        f.write(csv_data)

    return send_file('menus.csv', as_attachment=True)