class MongoConfig:
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT =  27017
    MONGO_DBNAME =  'smart_design_testapp_db'
    MONGO_URI = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}'