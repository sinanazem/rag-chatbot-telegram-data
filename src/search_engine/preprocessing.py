import copy
import re
from hazm import Normalizer, word_tokenize
import copy
import re
import demoji
from loguru import logger


class TextPreprocessor:
    def __init__(self, stopwords_file):
        self.normalizer = Normalizer()
        self.stop_words = self.load_stopwords(stopwords_file)
        
    def load_stopwords(self, file_path):
        logger.info(f"Loading stopwords from {file_path}")
        with open(file_path) as f:
            return {self.normalizer.normalize(line.strip()) for line in f}
        
    def remove_stopwords(self, text):
        tokens = word_tokenize(self.normalizer.normalize(text))
        return ' '.join(token for token in tokens if token not in self.stop_words)
    
    def de_emojify(self, text):
        # Remove certain Unicode characters and replace emojis
        pattern = re.compile(r"[\u2069\u2066]+", re.UNICODE)
        text = pattern.sub('', text)
        return demoji.replace(text, " ")
    
    def preprocess_text(self, message):
        text_content = ''
        if isinstance(message, list):
            for sub_message in message:
                if isinstance(sub_message, str):
                    text_content += f" {self.remove_stopwords(sub_message)}"
                elif isinstance(sub_message, dict) and sub_message.get('type') in {
                    'text_link', 'bold', 'italic', 'hashtag', 'mention', 'pre'
                }:
                    text_content += f" {self.remove_stopwords(sub_message['text'])}"
        else:
            text_content += f" {self.remove_stopwords(message)}"
        
        tokens = word_tokenize(self.normalizer.normalize(text_content))
        return tokens
    
    def preprocess(self, input_docs):
        processed_docs = copy.deepcopy(input_docs)
        for doc in processed_docs:
            if 'text' in doc and doc['text']:
                doc['text'] = self.preprocess_text(doc['text'])
        return processed_docs
    
    
if __name__ == "__main__":
    
    # sample Data
    data = [
        {
            'id': 6,
            'type': 'message',
            'date': '2021-07-05T23:26:28',
            'date_unixtime': '1625514988',
            'from': 'Sima',
            'from_id': 'user622339736',
            'reply_to_message_id': 2,
            'text': 'موافقم\nمن حتی نتونستم داخل کلاس جوین بشم آفلاین هم برام باز نشد',
            'text_entities': [{'type': 'plain',
            'text': 'موافقم\nمن حتی نتونستم داخل کلاس جوین بشم آفلاین هم برام باز نشد'}]
            },
        {
            'id': 9,
            'type': 'message',
            'date': '2021-07-05T23:26:37',
            'date_unixtime': '1625514997',
            'from': 'Sobhan Razyani',
            'from_id': 'user72383515',
            'reply_to_message_id': 4,
            'text': 'ممنونم. Jady؟',
            'text_entities': [{'type': 'plain', 'text': 'ممنونم. Jady؟'}]
            }
        ]
    
    preprocessor = TextPreprocessor('src/search_engine/stopwords.txt')
    pre_processed_data = preprocessor.preprocess(data)
    print(pre_processed_data[1])
    