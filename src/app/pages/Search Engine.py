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

def query_print(query, index, pre_processed_data, data, content=False, max_cnt=10):
    results = process_query(query, index, pre_processed_data)[:max_cnt]
    if len(results) == 0:
        st.write("نتیجه ای یافت نشد")
    for rank, doc in enumerate(results):
        if doc is None:
            continue
        st.write(50 * '=')
        st.write(f'Rank: {rank + 1}, docID: {doc}')
        for dict_ in data:
            if dict_["id"] == str(doc):
                st.write(f'From: {dict_["from"]}')
                st.write(f'Date: {dict_["date"]}')
                st.write(f'{dict_["text"]}')
                break


with open("src/search_engine/data/pre_processed_telegram_data.json", 'r') as f:
    pre_processed_data = json.load(f)
    
with open("src/search_engine/index_dir/index.json", 'r') as f:
    index = json.load(f)

uri = "mongodb://localhost:27017/"
database_name = "pytopia"
collection_name = "messages"
query = {}  # Fetch all documents

data = fetch_data_from_mongodb(uri, database_name, collection_name, query)

if st.button("search"):
    query_print(user_query, index, pre_processed_data, data)




