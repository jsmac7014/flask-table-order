from flask import Blueprint, render_template, request, session, redirect, jsonify
import datetime

from db.orders import create_order, create_orders_has_foods
from db.stores import get_stores_foods
from db.stores_tables import get_stores_tables

guest = Blueprint('guest', __name__)

@guest.route('/order/<stores_id>', methods=['GET', 'POST'])
def order(stores_id):
    # get menu from db
    menu = get_stores_foods(stores_id)
    tables = get_stores_tables(stores_id)

    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     email = request.form.get('email')
    #     phone = request.form.get('phone')
    #     address = request.form.get('address')
    #     print(name, email, phone, address)
    return render_template('guest/order.html', menu=menu, tables=tables, stores_id=stores_id)


@guest.route('/order-confirm/<stores_id>', methods=['GET'])
def order_confirm(stores_id):
    return render_template('guest/order-confirm.html', stores_id=stores_id)

@guest.route('/order/create', methods=['POST'])
def order_create():
    data = request.get_json()

    table_id = data['table_id']
    orders = data['order']

    orders_id = create_order({'order_date': datetime.datetime.now(), 'status': 'PENDING', 'stores_tables_id': table_id})
    if(orders_id is None):
        return jsonify({'result': 'fail'})

    result = create_orders_has_foods(orders, orders_id)
    if(result is False):
        return jsonify({'result': 'fail'})

    return jsonify({'result': 'success'})