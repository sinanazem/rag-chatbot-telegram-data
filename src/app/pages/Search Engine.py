import streamlit as st
from streamlit_lottie import st_lottie
import json
import datetime
# st.header("Pytopia Search Engine")
#st.image("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/app/static/img/pytopia-text.webp")


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
        
st.text_input("Search Message")





