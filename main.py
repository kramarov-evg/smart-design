from flask import Flask, request, jsonify
from bp import bp
from config import MongoConfig
from extensions import mongo

# Init app
app = Flask(__name__)
app.config.from_object(MongoConfig())
mongo.init_app(app)
app.register_blueprint(bp)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
