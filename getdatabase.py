from pymongo import MongoClient

def connect():
	conn = 'MONGO_API'
	mongo_client = MongoClient(conn)
	db = mongo_client.get_database('DATABASE')
	records = db.user_records
	return records
