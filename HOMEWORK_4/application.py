import os
import json
import requests

from flask import Flask, jsonify, render_template, request
from urllib.request import Request, urlopen
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html",
                           login_url=os.environ["LOGIN_URL"],
                           register_url=os.environ["REGISTER_URL"])


@app.route("/chat", methods=['GET'])
def chat():
    return render_template("chat.html", firebase_api_key=os.environ["FIREBASE_API_KEY"])

@app.route("/translate", methods=['POST'])
def translate():
    data = request.json
    headers = {
        'Ocp-Apim-Subscription-Key': 'afa0aa27aa644d62a85f1d31aa26ce4d',
        "Content-Type": "application/json"
    }

    print(data)
    
    url = "https://andreeaarsene.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es"
    r = Request(url, json.dumps(data).encode(), headers=headers)
    req = urlopen(r)
    
    return jsonify(json.loads(req.read().decode()))

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    headers = {
        'Ocp-Apim-Subscription-Key': 'e7894c840ce349edb4a8586b329d7244',
        "Content-Type": 'application/x-www-form-urlencoded'
    }

    params = {
        'mkt': 'en-us',
        'mode': 'proof'
    }

    url = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"
    r = requests.post(url, headers=headers, data=data, params=params)

    text = ""
    if r.status_code == 200:
        print(r.content)
        text = data["text"]
        content = json.loads(r.content)
        flagged_tokens = content['flaggedTokens']
        for token in flagged_tokens:
            print(token)
            text = text.replace(token["token"], token["suggestions"][0]["suggestion"])

    return jsonify({"spell_checked": text})


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


if __name__ == '__main__':
    app.run(debug=True)
