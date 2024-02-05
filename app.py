# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from wikipedia_data_fetcher import WikipediaDataFetcher
from search_history_manager import SearchHistoryManager

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Separated Database Logic
from dbmodel import db

db.init_app(app)

# Separated Wikipedia API Interaction
wikipedia_data_fetcher = WikipediaDataFetcher()

# Separated Search History Management
search_history_manager = SearchHistoryManager()

@app.route('/word_frequency', methods=['GET'])
def word_frequency():
    topic = request.args.get('topic')
    n = request.args.get('n')

    if not topic or not n:
        return jsonify({'error': 'Invalid input. Both topic and n are required.'}), 400

    try:
        n = int(n)
        if n <= 0:
            raise ValueError('Invalid value for n. Please provide a positive integer.')
    except ValueError as e:
        return jsonify({'error': f'Invalid value for n. {str(e)}'}), 400

    data = wikipedia_data_fetcher.fetch_wikipedia_data(topic)

    if not data or 'query' not in data or 'pages' not in data['query']:
        return jsonify({'error': 'Invalid topic. Wikipedia article not found.'}), 404

    page_id = list(data['query']['pages'].keys())[0]
    if 'title' not in data['query']['pages'][page_id]:
        return jsonify({'error': 'Failed to retrieve article details from Wikipedia.'}), 500

    article_text = data['query']['pages'][page_id]['extract']
    clean_text = wikipedia_data_fetcher.clean_article_text(article_text)

    if not clean_text:
        return jsonify({'error': 'Failed to retrieve clean article text from Wikipedia.'}), 500

    word_frequency_result = search_history_manager.analyze_word_frequency(clean_text, n)
    search_history_manager.save_search_history(topic, word_frequency_result)

    return jsonify({'word_frequency': word_frequency_result})

@app.route('/search_history', methods=['GET'])
def search_history():
    searches = search_history_manager.get_search_history()
    search_history_data = [{'topic': entry.topic, 'top_words': entry.top_words} for entry in searches]
    return jsonify({'search_history': search_history_data})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
