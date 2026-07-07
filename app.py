from flask import Flask
from flask import render_template
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from routes.auth import auth
from routes.vendors import vendors
from routes.orders import orders

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(vendors, url_prefix='/vendors')
    app.register_blueprint(orders, url_prefix='/orders')


    with app.app_context():
        db.create_all()

    # test route
    @app.route('/ping')
    def ping():
        return{'status':'alive','app':'snack_vendor'}
    @app.route('/')
    def index():
        return render_template('index.html')
    @app.route('/customer')
    def customer():
        return render_template('customer.html')
    @app.route('/vendor')
    def vendor_page():
        return render_template('vendor.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
