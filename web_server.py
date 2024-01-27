from flask import Flask, request
from resources import EntryManager, Entry
# Test
FOLDER = 'C:\\temp'
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries/")
def get_entries():
    result = list()
    entryManager = EntryManager(FOLDER)
    entryManager.load()
    for item in entryManager.entries:
        result.append(item.json())
    return result

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entryManager = EntryManager(FOLDER)
    iJson = request.get_json()
    for json_item in iJson:
        entryManager.entries.append(Entry('').from_json(json_item))
    entryManager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)