import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Union

import arabic_reshaper
import demoji
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bidi.algorithm import get_display
from hazm import Normalizer, sent_tokenize, word_tokenize
from loguru import logger
from PIL import Image
from tqdm import tqdm
from wordcloud import WordCloud


class ChatStatistics:
    """Generates chat statistics from a telegram chat json file
    """

    def __init__(self, chat_data):

        self.chat_data = chat_data

        self.normalizer = Normalizer()

        # load stopwords
        logger.info(f"Loading stopwords from {'stopwords.txt'}")
        stop_words = open('src/analytics/stopwords.txt').readlines()
        stop_words = map(str.strip, stop_words)
        self.stop_words = set(map(self.normalizer.normalize, stop_words))

    @staticmethod
    def rebuild_msg(sub_messages):
        msg_text = ''
        for sub_msg in sub_messages:
            if isinstance(sub_msg, str):
                msg_text += sub_msg
            elif 'text' in sub_msg:
                msg_text += sub_msg['text']

        return msg_text

    def msg_has_question(self, msg):
        """Checks if a message has a question

        :param msg: message to check
        """
        if not isinstance(msg['text'], str):
            msg['text'] = self.rebuild_msg(msg['text'])

        sentences = sent_tokenize(msg['text'])
        for sentence in sentences:
            if ('?' not in sentence) and ('؟' not in sentence):
                continue

            return True

    def get_top_users(self, top_n: int = 10) -> dict:
        """Gets the top n users from the chat.

        :param top_n: number of users to get, default to 10
        :return: dict of top users
        """
        # check messages for questions
        is_question = defaultdict(bool)
        for msg in self.chat_data:
            if not msg.get('text'):
                continue

            if not isinstance(msg['text'], str):
                msg['text'] = self.rebuild_msg(msg['text'])

            sentences = sent_tokenize(msg['text'])
            for sentence in sentences:
                if ('?' not in sentence) and ('؟' not in sentence):
                    continue
                is_question[msg['id']] = True
                break

        # get top users based on replying to questions from others
        logger.info("Getting top users...")
        users = []
        for msg in self.chat_data:
            if not msg.get('reply_to_message_id'):
                continue
            if is_question[msg['reply_to_message_id']] is False:
                continue
            users.append(msg['from'])

        top_users = dict(Counter(users).most_common(top_n))
        return [{"user":user, "message_count":message_count} for user, message_count in top_users.items()]

    def remove_stopwords(self, text):
        """Removes stop-words from the text.

        :param text: Text that may contain stop-words.
        """
        tokens = word_tokenize(self.normalizer.normalize(text))
        tokens = list(filter(lambda item: item not in self.stop_words, tokens))
        return ' '.join(tokens)

    def de_emojify(self, text):
        """Removes emojis and some special characters from the text.

        :param text: Text that contains emoji
        """
        regrex_pattern = re.compile(pattern="[\u2069\u2066]+", flags=re.UNICODE)
        text = regrex_pattern.sub('', text)
        return demoji.replace(text, " ")

    def generate_word_cloud(
        self,
        output_dir: Union[str, Path],
        generate_from_frequencies: bool = False,
        width: int = 800, height: int = 600,
        max_font_size: int = 250,
        background_color: str = 'white',
        mask_image_path: Union[str, Path] = None,
    ):
        """Generates a word cloud from the chat data

        :param output_dir: path to output directory for word cloud image and top user statistics.
        """
        logger.info("Loading text content...")
        text_content = ''
        for message in tqdm(self.chat_data, 'Processing messages...'):
            if not message.get('text'):
                continue

            msg = message['text']
            if isinstance(msg, list):
                for sub_msg in msg:
                    if isinstance(sub_msg, str):
                        text_content += f" {self.remove_stopwords(sub_msg)}"
                    elif isinstance(sub_msg, dict) and sub_msg['type'] in {
                        'text_link', 'bold', 'italic',
                        'hashtag', 'mention', 'pre'
                    }:
                        text_ = self.remove_stopwords(sub_msg['text'])
                        text_content += f" {text_}"
            else:
                text_content += f" {self.remove_stopwords(msg)}"

        if mask_image_path:
            logger.info(f"Loading mask image from {mask_image_path}...")
            mask = np.array(Image.open(mask_image_path))
        wordcloud = WordCloud(
            width=width, height=height,
            font_path=str('src/analytics/font.ttf'),
            background_color=background_color,
            max_font_size=max_font_size,
        )

        if generate_from_frequencies:
            tokens = list(word_tokenize(self.normalizer.normalize(text_content)))
            top_n_words = dict(Counter(tokens).most_common(100))

            reshaped_tokens_count = defaultdict(int)
            for token, count in top_n_words.items():
                token = arabic_reshaper.reshape(self.de_emojify(token))
                token = get_display(token)
                reshaped_tokens_count[token] = reshaped_tokens_count.get(token, 0) + count

            logger.info("Generating word cloud...")
            wordcloud.generate_from_frequencies(top_n_words)
        else:
            text_content = arabic_reshaper.reshape(self.de_emojify(text_content))
            # text_content = get_display(text_content)

            logger.info("Generating word cloud...")
            wordcloud.generate(text_content)

        logger.info(f"Saving word cloud to {output_dir}")
        # wordcloud.to_file(str(Path(output_dir) / 'word_cloud.png'))
        return wordcloud

