from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError


mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)
    return mongo.db

def get_collection(name):
    db = mongo.db
    try:
        if name not in db.list_collection_names():
            db.create_collection(name)
            print("Created collection: telemetry")
        return db[name]
    except PyMongoError as e:
        print(f"[DB ERROR] Cannot access or create collection '{name}': {e}")
        return None


