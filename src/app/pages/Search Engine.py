import streamlit as st
from streamlit_lottie import st_lottie
import json
import datetime
# st.header("Pytopia Search Engine")
#st.image("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/app/static/img/pytopia-text.webp")
from src.search_engine.index_search import process_query
from src.mongo_analytics.load import fetch_data_from_mongodb


import streamlit as st
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.image("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/app/static/img/pytopia-text.webp", width=220)
    


kpmg_col1, kpmg_col2 = st.columns([1, 2])
with kpmg_col2: 
    @st.cache_data
    def load_lottiefile(filepath: str):
        with open(filepath,"r") as f:
            return json.load(f)
    lottie11 = load_lottiefile("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/app/static/animations/Animation - 1717623105209.json")
    st_lottie(lottie11,key='locMainImage', height=350)

with kpmg_col1:
    st.markdown('### Pytopia Search Engine')
    
    st.markdown(
        """ GroupSearch makes finding information in Telegram groups easy and fast.
        With smart indexing and intelligent search, you can quickly locate messages,
        files, and links."""
    )
    st.markdown(
        """
        Enjoy real-time updates and secure, private searches.
        Upgrade your Telegram experience with GroupSearch today!
        """
        )
    
import streamlit as st

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.write('**Start Date**')
    start_date = st.date_input('Start date', datetime.date(2022, 1, 2))

with col2:
    st.write('**End Date**')
    end_date = st.date_input('End date', datetime.date(2022, 1, 2))



with col3:
    st.write('**Name**')
    name = st.text_input('All Messages from ...')


with col4:
    st.write("")

    if st.button('Filter'):
        pass
        
user_query = st.text_input("Search Message")

uri = "mongodb://localhost:27017/"
database_name = "pytopia"
collection_name = "messages"
query = {}  # Fetch all documents

from src.search_engine.index_search import process_query
from src.mongo_analytics.load import fetch_data_from_mongodb
from src.search_engine.indexsearch import process_query
import json


def query_streamlit(user_query, uri, database_name, collection_name, query_db={}):

    data = fetch_data_from_mongodb(uri, database_name, collection_name, query_db)
    
    with open("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/search_engine/data/pre_processed_telegram_data.json", 'r') as f:
        pre_processed_data = json.load(f)
    
    with open("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/search_engine/index_dir/index.json", 'r') as f:
        index = json.load(f)
        
    match_search_id_list = process_query(user_query)
    
    def find_msg(msg_id_list):
        list_ = []
        for data_dict in data:
            if str(data_dict["id"]) in msg_id_list:
                list_.append({"From": data_dict['from'], "Date":data_dict['date'], "Text":data_dict['text']}) 
        return list_
    return find_msg(match_search_id_list)


if st.button("search"):
    with st.spinner('Loading data...'):
        result_list = query_streamlit(user_query, uri, database_name, collection_name, query_db={})
        for chat in result_list:
            if isinstance(chat["Text"], str):
                st.info(f'{chat["From"]} | {chat["Date"]}')
                st.warning(chat["Text"])
        
    
    




