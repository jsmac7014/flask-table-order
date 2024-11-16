from datetime import datetime
from flask import jsonify, request
from flask_socketio import SocketIO, emit, join_room
from db.orders import create_order, create_orders_has_foods
from db.stores_tables import get_stores_tables_name
from views.admin import order

socketio = SocketIO()

def initialize_socket(app):
    socketio.init_app(app)

    @socketio.on('connect')
    def connect():
        print('Client connected')
        emit('connected', {'data': 'Connected'})

    @socketio.on('disconnect')
    def disconnect():
        print('Client disconnected')
        emit('disconnected', {'data': 'Disconnected'})

    @socketio.on('join.admin')
    def join_admin(data):
        store_id = data.get('store_id')
        if store_id:
            room_name = f'stores_{store_id}'
            join_room(room_name)
            emit('admin.joined', {'message': f'Joined admin room for store {store_id}'}, room=request.sid)

    @socketio.on('create.order')
    def handle_create_order(data):
        table_id = data['table_id']
        orders = data['order']
        order_date = datetime.now()

        orders_id = create_order({
            'order_date': order_date,
            'status': 'PENDING',
            'stores_tables_id': table_id
        })

        if orders_id is None:
            emit('created.order', {'result': 'fail'}, room=request.sid)
            return

        result = create_orders_has_foods(orders, orders_id)

        if not result:
            emit('created.order', {'result': 'fail'}, room=request.sid)
            return

        emit('created.order', {'result': 'success'}, room=request.sid)


        # get table name by table_id
        table_name = get_stores_tables_name(table_id)
        # Notify admin
        # admin_data
        admin_data = {
            'order_date': order_date.isoformat(),
            'status': 'PENDING',
            'orders_id': orders_id,
            'table_id': table_id,
            'name': table_name
        }

        store_room_name = f'stores_{data["stores_id"]}'
        emit('created.order.admin', {'result': 'success', 'data': admin_data}, room=store_room_name)

    return socketio
