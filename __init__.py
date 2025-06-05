from flask import Flask

def create_app():
    app = Flask(__name__)
    # In a real application, you might load configuration here
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from . import routes

        # Register Blueprints (if any)
        # app.register_blueprint(bp_name)

    return app
