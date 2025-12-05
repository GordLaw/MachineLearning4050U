from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/query", methods=["POST"])
def query_model(query_data=None):
    return 0

@app.route("/get-top-games", methods=["GET"])
def get_top_games():
    store_params = {
        "filter": "globaltopsellers",
        "ignore_preferences": "1",
        "category1": "998",
        "descids%5B%5D": "3",
        "json": "1",
    }
    top_games_json = requests.get("https://store.steampowered.com/search/results/", params=store_params)
    games_list = []
    for item in top_games_json.json()["items"][:20]:
        
        games_list.append({
            "logo": item["logo"],
            "name": item["name"],
        })
    return jsonify({
        "status": 200,
        "top_games": games_list
    })

@app.route("/get-game-page/<game_name>", methods=["GET"])
def get_game_page(game_name: str):
    item_params = {
        "term": game_name,
        "l": "english",
        "cc": "CA"
    }
    item_search = requests.get("https://store.steampowered.com/api/storesearch/", params=item_params)
    game_id = item_search.json()["items"][0]["id"]
    game_page = f"https://store.steampowered.com/app/{game_id}/"
    return jsonify({
        "status": 200,
        "game_page": game_page
    })

@app.route("/get-game-genre/<genre>", methods=["GET"])
def get_game_genre(game_genre: str):
    genre_params = {
        "term": game_genre,
        "l": "english",
        "cc": "CA"
    }
    genre_search = requests.get("https://store.steampowered.com/api/getappsingenre/", params=genre_params)

@app.route("/get-featured-games", methods=["GET"])
def get_featured_game():
    featured_search = requests.get("https://store.steampowered.com/api/featured")
    featured_game_list = featured_search.json()["large_capsules"]

if __name__ == "__main__":
    print("Starting Flask app...")
    print("Model will load in the background...")
    app.run(host="0.0.0.0", port=8080, debug=False)