from pymongo import MongoClient

def fetch_data_from_mongodb(uri, database_name, collection_name, query={}):
    # Connect to the MongoDB server
    client = MongoClient(uri)
    
    # Select the database
    db = client[database_name]
    
    # Select the collection
    collection = db[collection_name]
    
    # Fetch data (find returns a cursor, converting it to a list of dictionaries)
    data = list(collection.find(query))
    
    # Optionally, remove the '_id' field if it's not needed
    for document in data:
        if '_id' in document:
            del document['_id']
    
    return data
