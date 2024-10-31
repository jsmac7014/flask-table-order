from flask import Blueprint, render_template, request, session, redirect

guest = Blueprint('guest', __name__)

@guest.route('/guest/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        print(name, email, phone, address)
    return render_template('guest/order.html')

