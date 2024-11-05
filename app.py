import json
from flask import Flask, Response, jsonify
import time as t

from db.orders import get_new_orders, get_last_orders_id
from views.admin import admin
from views.guest import guest
from datetime import datetime, date, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(guest, url_prefix='/guest')

# @app.route('/order/stream/<stores_id>')
# def stream_orders(stores_id):
#
#     def event_stream():
#         with app.app_context():
#             last_orders_id = get_last_orders_id(stores_id)
#             print("last_orders_id :", last_orders_id)
#             while True:
#                 try:
#                     new_order = get_new_orders(stores_id, last_orders_id)
#                     if new_order:
#                         for order in new_order:
#                             last_orders_id = order['orders_id']
#
#                             yield 'data: %s\n\n' % json.dumps(new_order, default=_datetime_handler)
#                             t.sleep(2)
#
#                 except Exception as e:
#                     print('error', e)
#                     break
#
#     return Response(event_stream(), content_type='text/event-stream')




def _datetime_handler(obj):
    if isinstance(obj, (datetime, date, time)):
        return str(obj)

if __name__ == '__main__':
    app.run(debug=True)