from flask import Flask, request, jsonify
from config.settings import URL_MAP
import hashlib
import random
import string
import datetime
from utils.hashed_url import generate_hash

app = Flask(__name__)

def generate_hash(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:6]

@app.route('/generate', methods=['POST'])
def generate_hashed_url():
    """This method generates the hashed url for original url.
    example payload:
    {
        "url": "http://sample.info/?insect=fireman&porter=attraction#cave"
    }
    response: 
    {
        "hashed_url": "0984ff"
    }
    """
    data = request.json
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    hashed_url = generate_hash(original_url)
    privacy_aware = data.get('privacy_aware', False)

    URL_MAP[hashed_url] = {
        'original_url': original_url,
        'clicks': 0,
        'created_at': datetime.datetime.now(),
        'expiration_date': None,
        'privacy_aware': privacy_aware
    }

    return jsonify({'hashed_url': hashed_url}), 201

@app.route('/<hashed_url>', methods=['GET'])
def redirect_to_original_url(hashed_url):
    """
    this method redirects to original url using hashed_url.
    response: code: 302 found if the hashed_url is correct.
    response: 
    {
        "original_url": "http://sample.info/?insect=fireman&porter=attraction#cave"
    }
    """
    if hashed_url not in URL_MAP:
        return jsonify({'error': 'Hashed URL not found'}), 404

    original_url = URL_MAP[hashed_url]['original_url']
    URL_MAP[hashed_url]['clicks'] += 1

    # Add logic here for privacy-awareness if needed

    return jsonify({'original_url': original_url}), 302
