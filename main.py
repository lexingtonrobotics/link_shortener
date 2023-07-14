from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string
import json

app = Flask(__name__)


def generate_short_url():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

@app.route('/', methods=['GET'])
def give_short_url():
    long_url = request.args.get('url')
    if not long_url:
        return 'Missing URL parameter - Bad Request', 400
    short_url = generate_short_url()
    with open('urls.json', 'r') as file:
        SHORTENED_URLS = json.load(file)
    SHORTENED_URLS[short_url] = long_url
    with open('urls.json', 'w') as file:
        file.write(json.dumps(SHORTENED_URLS))
        
    return f'{request.url_root}protocol/{short_url}'

@app.route('/protocol/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    try :
        with open('urls.json', 'r') as file:
            SHORTENED_URLS = json.load(file)
        long_url = SHORTENED_URLS[short_url]
        return redirect(long_url)
    except KeyError:
        return 'URL not found', 404


if __name__ == '__main__':
    app.run(debug=True)