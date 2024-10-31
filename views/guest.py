from flask import Blueprint, render_template, request, session, redirect, jsonify

from db.stores import get_stores_foods

guest = Blueprint('guest', __name__)

@guest.route('/order/<stores_id>', methods=['GET', 'POST'])
def order(stores_id):
    # get menu from db
    menu = get_stores_foods(stores_id)

    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     email = request.form.get('email')
    #     phone = request.form.get('phone')
    #     address = request.form.get('address')
    #     print(name, email, phone, address)
    return render_template('guest/order.html', menu=menu)

