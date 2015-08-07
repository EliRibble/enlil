from flask import Flask
import enlil.api.root

def create_app(config):
    app = Flask('enlil')
    app.register_blueprint(enlil.api.root.blueprint)
    return app
