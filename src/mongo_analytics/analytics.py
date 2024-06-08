from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime


def get_top_users(mongo_uri, db_name, collection_name, start_date, end_date, top_n=0):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Aggregation pipeline to count messages per user
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lt": end_date
                }
            }
        },
        {
            "$group": {
                "_id": "$from",  # Group by the 'from' field (username)
                "count": {"$sum": 1}  # Count the number of messages per user
            }
        },
        {
            "$sort": {"count": -1}  # Sort by count in descending order
        },
        {
            "$limit": top_n  # Limit to top N users
        }
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)

    # Format the results as a list of dictionaries
    top_users = [{"user": result["_id"], "message_count": result["count"]} for result in results]

    return top_users


def get_message_counts_by_date(mongo_uri, db_name, collection_name, start_date, end_date):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Convert date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')

    # Aggregation pipeline to count messages per day
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_datetime.isoformat(),
                    "$lt": end_datetime.isoformat()
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": {"$dateFromString": {"dateString": "$date"}}
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)

    # Format the results as a list of dictionaries
    message_counts = [{"date": result["_id"], "count": result["count"]} for result in results]

    return message_counts


def get_question_counts_by_user(mongo_uri, db_name, collection_name, start_date, end_date):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Convert date strings to datetime objects
    # start_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    # end_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')

    # Aggregation pipeline to count questions per user
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lt": end_date
                },
                "text": {"$regex": r"\?|؟$"}  # Match messages ending with a question mark
            }
        },
        {
            "$group": {
                "_id": "$from",  # Group by the 'from' field (username)
                "count": {"$sum": 1}  # Count the number of questions per user
            }
        },
        {
            "$sort": {"count": -1}  # Sort by count in descending order
        },
        {
            "$limit": 50  # Limit the results to the top 50 users
        }
    ]

    # Execute the aggregation pipeline
    results = list(collection.aggregate(pipeline))

    # Format the results as a list of dictionaries
    question_counts = [{"user": result["_id"], "question_count": result["count"]} for result in results]

    return question_counts


