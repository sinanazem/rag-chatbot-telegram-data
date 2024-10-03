import streamlit as st
import json
import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure, DocumentTooLarge

# Page configuration
st.set_page_config(layout="wide")

# Sidebar setup
st.sidebar.header("Upload Chat History")
st.image("https://pairroxz.com/blog/wp-content/uploads/2023/05/Cost-of-Developing-an-App-Like-Telegram-in-2023.png", width=550)

# MongoDB configuration
# MONGO_URI = "mongodb://sinanazem:sinanazem@localhost:27017/messages"
DB_NAME = "chat_db"  # Replace with your database name
COLLECTION_NAME = "chat_data"  # Replace with your collection name

# Initialize MongoDB
def init_mongo(db_name, collection_name):
    try:
        client = MongoClient()
        db = client[db_name]
        collection = db[collection_name]
        # Test connection
        client.admin.command('ping')
        return collection
    except OperationFailure as e:
        st.sidebar.error(f"Failed to connect to MongoDB: {e}")
        st.stop()  # Stop execution if connection fails

collection = init_mongo(DB_NAME, COLLECTION_NAME)

# Functions for MongoDB operations
def save_data_to_mongodb(collection, data):
    try:
        collection.insert_one(data)
    except DocumentTooLarge:
        # Split data into smaller parts if the whole document is too large
        split_and_save_data(collection, data)
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")

def split_and_save_data(collection, data):
    messages = data.get("messages", [])
    chunk_size = 1000  # Adjust based on the size of each individual message
    for i in range(0, len(messages), chunk_size):
        chunk = messages[i:i + chunk_size]
        chunk_data = {"messages": chunk}
        collection.insert_one(chunk_data)

def load_data_from_mongodb(collection):
    return list(collection.find())

# Load existing data from MongoDB when the app starts
if "chat_data" not in st.session_state:
    st.session_state["chat_data"] = load_data_from_mongodb(collection)

# File uploader and handler
data = st.sidebar.file_uploader(label="Upload Telegram Group Chat History (JSON format): ")

if data is not None:
    try:
        new_data = json.load(data)
        st.sidebar.success("File uploaded successfully!")
        
        # Add new data to MongoDB and session state
        save_data_to_mongodb(collection, new_data)
        st.session_state["chat_data"].append(new_data)
    except json.JSONDecodeError:
        st.sidebar.error("Uploaded file is not a valid JSON.")
    except DocumentTooLarge as e:
        st.sidebar.error(f"Document too large: {e}")
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
else:
    st.sidebar.write("Please upload a file to get started.")

# Main page for search
st.header("Telegram Chat Search Engine")
search_term = st.text_input("Enter a search term:")

# Function to search chat data
def search_chat_data(chat_data, search_term):
    if not search_term:
        return []
    search_term_lower = search_term.lower()
    results = [
        message
        for chat in chat_data
        for message in chat.get("messages", [])
        if search_term_lower in str(message.get("text", "")).lower()
    ]
    return results

if search_term:
    results = search_chat_data(st.session_state["chat_data"], search_term)
    st.subheader(f"Search Results for '{search_term}':")
    if results:
        for result in results:
            st.write(result)
    else:
        st.write("No results found.")
