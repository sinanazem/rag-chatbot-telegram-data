import streamlit as st
from streamlit_lottie import st_lottie
import json
import datetime

from src.mongo_analytics.analytics import get_top_users, get_message_counts_by_date
from src.mongo_analytics.filter_data import filter_telegram_chats
from src.analytics.stats import ChatStatistics
from src.visualizations.plot import plot_top_users, plot_message_counts, plot_top_users_donut



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
with kpmg_col1: 

        st.image("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/app/static/img/Visual data-cuate.png", width=350)

with kpmg_col2:
    st.markdown("""
    # 📊 Telegram Chat Analysis Dashboard

    - **🔍 Overview**: Analyze your Telegram chat data with interactive visualizations.
    - **📊 Features**:
    - **📈 Bar Plot**: Message frequency by participants.
    - **📉 Line Plot**: Trend of messages over time.
    - **🍩 Donut Plot**: Distribution of message types.
    - **☁️ Word Cloud**: Most frequently used words.
    - **🛠️ User Interaction**: Filter data, explore trends, and gain insights.
    - **👍 Usage**: Intuitive interface with real-time analysis.
    """)
    
# Title
st.write('#### Upload or select your Telegram Chat Data (JSON file)')

# Tabs for upload or select
t1, t2 = st.tabs(['UPLOAD', 'SELECT'])

# File uploader tab
with t1:
    uploaded_file = st.file_uploader('Upload a JSON file', type='json', key='json_file', label_visibility="collapsed")

# File select tab
with t2:
    selected_file = st.selectbox('Select a file', ["filenames1.json", "filenames2.json"], key='selected_file', label_visibility="collapsed")

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.write('**Start Date**')
    start_date_input = st.date_input('Start date', start_date)

with col2:
    st.write('**End Date**')
    end_date_input = st.date_input('End date', end_date)



with col3:
    st.write('**Name**')
    name = st.text_input('All Messages from ...')


with col4:
    st.write("")

    if st.button('Filter'):
        pass
        


start_date = start_date_input.strftime('%Y-%m-%dT%H:%M:%S')
end_date = end_date_input.strftime('%Y-%m-%dT%H:%M:%S')

mongo_uri = "mongodb://localhost:27017/"
db_name = "pytopia"
collection_name = "messages"




# Button to generate dashboard
# if st.button('Generate Dashboard'):
#     if uploaded_file is not None:
#         # Process the uploaded file
#         st.write("Processing uploaded file...")
#         # Your code to handle the uploaded file goes here
#         # ...
#     elif selected_file:
#         # Process the selected file
#         st.write(f"Processing selected file: {selected_file}")
#         # Your code to handle the selected file goes here
#         # ...
#     else:
#         st.write("Please upload or select a file to generate the dashboar")


if st.button('Generate Dashboard'):
    
    st.markdown("## Analytics Dashboard:")
    
    col1_user, col2_user = st.columns([1, 2])

    with col1_user:
        
        docs = filter_telegram_chats(start_date=start_date,
                                    end_date=end_date,
                                    db_name= db_name,
                                    collection_name=collection_name
                                    )
        obj = ChatStatistics(docs)

        st.plotly_chart(plot_top_users(obj.get_top_users()))

    with col2_user:
    
        wordcloud = obj.generate_word_cloud(output_dir='.', width=1800, height=1000)
        st.image(wordcloud.to_array())
        
    
    message_counts =  get_message_counts_by_date(mongo_uri, db_name, collection_name, start_date, end_date)
    st.plotly_chart(plot_message_counts(message_counts))


    col1_top_user, col2_top_user = st.columns([1, 2])

    with col1_top_user:
        
        top_users = get_top_users(mongo_uri, db_name, collection_name, top_n=20, start_date=start_date, end_date=end_date)

        st.plotly_chart(plot_top_users(top_users))

    with col2_top_user:
        
        top_users = get_top_users(mongo_uri, db_name, collection_name, top_n=6, start_date=start_date, end_date=end_date)

        st.plotly_chart(plot_top_users_donut(top_users))
        
        

        


