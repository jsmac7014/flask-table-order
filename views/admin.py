from flask import Blueprint, render_template, request, session, redirect, jsonify, Response, current_app
from werkzeug.utils import secure_filename

from db.auth import sign_in_admin_user, sign_up_admin_user, check_admin_user_with_stores_id
from db.orders import get_last_orders_id, get_new_orders, get_orders_list, get_orders_detail
from db.stores import create_store, get_stores_categories, get_stores_foods, create_store_foods, get_stores_foods_detail
from db.stores_tables import get_stores_tables, create_stores_tables, get_stores_tables_detail

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
    return render_template('admin/menu/menu-edit.html', detail=detail, menu_id=menu_id)


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


@admin.route('/order')
def order():
    if not is_logged_in():
        return redirect('/admin/sign-in')
    stores_id = session['stores_id']
    orders_list = get_orders_list(stores_id)

    return render_template('admin/order/order.html', orders=orders_list)

@admin.route('/order/detail/<order_id>', methods=['POST'])
def order_detail(order_id):
    if not is_logged_in():
        return redirect('/admin/sign-in')

    data = request.get_json()

    orders_id = data['orders_id']
    stores_id = session['stores_id']

    orders = get_orders_detail(orders_id, stores_id)
    return jsonify(orders)


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
    return render_template('admin/table/table-detail.html', table=table)
