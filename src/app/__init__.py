# app/__init__.py
from flask import Flask
from azure.cosmos import CosmosClient
from .routes import app as routes_app

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # cosmos_client = CosmosClient(app.config['COSMOS_ENDPOINT'], app.config['COSMOS_KEY'])
    # database = cosmos_client.get_database_client(app.config['COSMOS_DATABASE'])
    # container = database.get_container_client(app.config['COSMOS_CONTAINER'])

    # app.container = container

    app.register_blueprint(routes_app)

    return app