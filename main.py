from flask import Flask
from Routes import main_bp, auth_bp
from database.db import session

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'


# Registrar Blueprints
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)