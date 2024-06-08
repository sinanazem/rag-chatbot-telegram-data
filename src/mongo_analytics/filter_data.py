from pymongo import MongoClient
from bson.objectid import ObjectId


def filter_telegram_chats(start_date, end_date, name=None, from_id=None, db_name='pytopia', collection_name='messages'):  
    # Initialize MongoDB client and select the database and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]  
    # Build the query
    query = {
        'date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }
    
    if name:
        query['from'] = name
    
    if from_id:
        query['from_id'] = from_id

    # Execute the query
    results = collection.find(query)
    
    # Convert results to a list
    results_list = list(results)
    
    # Close the MongoDB client connection
    client.close()
    
    return results_list
