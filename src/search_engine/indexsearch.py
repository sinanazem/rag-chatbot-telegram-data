import re
import json
from src.search_engine.create_index import create_index_dict
from src.search_engine.preprocessing import TextPreprocessor
from src.mongo_analytics.load import fetch_data_from_mongodb
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


with open("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/search_engine/index_dir/index.json", 'r') as f:
    index = json.load(f)
    
with open("/mnt/c/Users/user/OneDrive/Desktop/rag-chatbot-telegram-data/src/search_engine/data/pre_processed_telegram_data.json", 'r') as f:
    pre_processed_docs = json.load(f)

def simple_process(docs, tokens):
    docs_score = {}
    for token in tokens:
        if token in index:
            for doc_id in index[token]['docs']:
                    if doc_id not in docs_score.keys():
                        docs_score[doc_id] = 1
                    else:
                        docs_score[doc_id] += 1
   
    docs_score = sorted(docs_score.items(), key=lambda doc_score: doc_score[1], reverse=True)
    result = [x for x,_ in docs_score]
    return result


def exceptions_process(docs, tokens):
    removal_docs = []
    for token in tokens:
        rmv_docIds = index[token]['docs'].keys()
        for doc_id in rmv_docIds:  
             if removal_docs.count(doc_id) == 0:
                    removal_docs.append(doc_id)

    result = []            
    for doc_id in docs:
        if removal_docs.count(doc_id) == 0:
            result.append(doc_id)

    return result

def doc_contain_phrase(docId, phrase):
   # we need just a sequence of numbers in positions to find a doc contain special phrase",
    tokens_lst = phrase.split()
    positions = []
    for token in tokens_lst:
        positions.append(list(index[token]['docs'][docId]['positions']))

    for i in range (len(positions[0])):
        flag = True
        index_of_first_token = positions[0][i]
        for j in range (len(positions)):
            if positions[j].count(index_of_first_token + j) == 0:
                flag = False
        if flag :
            return True
    return flag

def phrasal_process(docs, phrases):
    posting_lists = []
    result = []
    for phrase in phrases:
        words = phrase.split()
        for word in words:
            if word in index:
                posting_lists.append(list(index[word]['docs'].keys()))
    
        intersection_doc_ids = set.intersection(*map(set, posting_lists))

        for docId in intersection_doc_ids:
            if doc_contain_phrase(docId, phrase):     
                result.append(docId)
    return result


def process_query(query):
    
    exception_tokens = re.findall(r'\!\s(\w+)', query)
    phrasal_tokens = re.findall(r'"([^"]*)"', query)
    raw_tokens = re.sub(r'\!\s\w+', '', query)
    raw_tokens = re.sub(r'"[^"]*"', '', raw_tokens)
    
    preprocessor = TextPreprocessor(ROOT_DIR/'stopwords.txt')
    simple_tokens = preprocessor.preprocess_text(raw_tokens)
    print(exception_tokens, phrasal_tokens, raw_tokens)
    result = None
    # sorted documents by relevance after processing simple tokens\n",
    if len(simple_tokens) > 0:
        result = simple_process(pre_processed_docs, simple_tokens)
        
    # removing the items that included exception tokens, kind of post filter
    if len(exception_tokens) > 0:
        removed_result = exceptions_process(result, exception_tokens)
        if len(removed_result) > 0 and len(result) > 0:
            result = [x for x in result if x in removed_result]  
            
    # Intersect of results with those containing phrasal queries\n",
    if len(phrasal_tokens) > 0:
        phrasal_result = phrasal_process(pre_processed_docs, phrasal_tokens)
        
        if result is None or len(result) == 0:
            return phrasal_result
        result = [x for x in result if x in phrasal_result]  

    return result
