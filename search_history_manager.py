# search_history_manager.py
import nltk
nltk.download('stopwords')
from collections import Counter
from dbmodel import db,SearchHistory
from nltk.corpus import stopwords

class SearchHistoryManager:
    @staticmethod
    def analyze_word_frequency(article_text, n):
        # Split the article text into words
        words = article_text.split()

        # Use Counter to count the frequency of each word

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

        word_frequency = Counter(filtered_words).most_common(n)

        return word_frequency

    @staticmethod
    def save_search_history(topic, word_frequency_result):
    # Convert the word frequency result to a string before saving
        top_words_str = ', '.join([f'{word}: {count}' for word, count in word_frequency_result])

        # Create a new SearchHistory entry and add it to the session
        search_entry = SearchHistory(topic=topic, top_words=top_words_str)
        db.session.add(search_entry)
        
        # Commit the changes to the database
        db.session.commit()

    @staticmethod
    def get_search_history():
        searches = SearchHistory.query.all()
        return searches
