from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db

from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.sale_routes import sale_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(sale_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)