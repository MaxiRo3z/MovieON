from flask import Flask
from Routes import main_bp, auth_bp

app = Flask(__name__)
app.config.from_pyfile('.env')

# Registrar Blueprints
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)