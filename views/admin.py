from flask import Blueprint, render_template, request, session, redirect

from db.auth import sign_in_admin_user, sign_up_admin_user
from db.stores import create_store, get_stores_categories, get_stores_foods, create_store_foods

from s3_connect import connect

admin = Blueprint('admin', __name__)

def is_logged_in():
    return session.get('logged_in')

@admin.route('/')
def dashboard():
    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/dashboard.html')

@admin.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if is_logged_in():
        return redirect('/admin')

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
            return redirect('/admin')
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

        return redirect('/admin')
    return render_template('admin/auth/sign-up.html')


@admin.route('/sign-out')
def sign_out():
    session.clear()
    return redirect('/admin/sign-in')


@admin.route('/upload', methods=['POST'])
def upload():
    if not is_logged_in():
        return redirect('/admin/sign-in')

    file = request.files['file']
    s3 = connect()
    s3.put_object(Bucket='table-order', Key=file.filename, Body=file)
    # get url of the uploaded file
    url = s3.generate_presigned_url('get_object', Params={'Bucket': 'table-order', 'Key': file.filename})
    print(url)
    # s3.upload_fileobj(file, 'table-order', file.filename)
    return redirect('/admin')

@admin.route('/menu')
def menu():
    categories = get_stores_categories(session['stores_id'])
    menus = get_stores_foods(session['stores_id'])

    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/menu.html', menus=menus, categories=categories)

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
    return render_template('admin/order.html')