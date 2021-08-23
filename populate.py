from flask import Flask
from extensions import mongo
from config import MongoConfig

if __name__ == "__main__":
    mongo.init_app
    app = Flask(__name__)
    app.config.from_object(MongoConfig())
    mongo.init_app(app)
    item1 = {
        'name': 'Item1',
        'description': 'First Item',
        'params': {
            'param1': 1,
            'param2': 'b'
        }
    }
    item2 = {
        'name': 'Item2',
        'description': 'Second Item',
        'params': {
            'param1': 10,
            'param2': 'beta'
        }
    }
    mongo.db.products.insert_many([item1, item2])
