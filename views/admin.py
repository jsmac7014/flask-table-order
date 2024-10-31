from flask import Blueprint, render_template, request, session, redirect

from database import sign_in_admin_user, sign_up_admin_user, get_store_menu, create_store

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
    #dummy category data
    categories = [
        {'name': '커피'},
        {'name': '음료'},
        {'name': '디저트'},
    ]
    # dummy menu data
    menus = [
        {'name': '아메리카노', 'price': 3000},
        {'name': '카페라떼', 'price': 4000},
        {'name': '카푸치노', 'price': 4000},
        {'name': '바닐라라떼', 'price': 4500},
        {'name': '카라멜마끼아또', 'price': 4500},
    ]

    # menu = get_store_menu()
    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/menu.html', menus=menus, categories=categories)


@admin.route('/order')
def order():
    if not is_logged_in():
        return redirect('/admin/sign-in')
    return render_template('admin/order.html')