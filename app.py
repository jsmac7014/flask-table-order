from flask import Flask

from views.admin import admin
from views.guest import guest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(guest, url_prefix='/guest')

if __name__ == '__main__':
    app.run(debug=True)