from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data storage
authors = ["John Doe", "Jane Smith"]
magazines = ["Tech World", "Foodie"]
articles = []  # A list of dictionaries to store articles

# Root Endpoint
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Magazine API!"})

# Endpoint: GET /authors
@app.route("/authors", methods=["GET"])
def get_authors():
    return jsonify(authors)

# Endpoint: GET /magazines
@app.route("/magazines", methods=["GET"])
def get_magazines():
    return jsonify(magazines)

# Endpoint: POST /add_article
@app.route("/add_article", methods=["POST"])
def add_article():
    # Get JSON data from request body
    data = request.get_json()

    # Validate required fields
    if not data or not all(k in data for k in ("author", "magazine", "title")):
        return jsonify({"error": "Invalid input, 'author', 'magazine', and 'title' are required"}), 400

    author = data["author"]
    magazine = data["magazine"]
    title = data["title"]

    # Validate input values
    if author not in authors or magazine not in magazines:
        return jsonify({"error": "Author or Magazine does not exist"}), 400

    # Add the article to the list
    articles.append({"author": author, "magazine": magazine, "title": title})
    return jsonify({"message": f"Article '{title}' added successfully!"}), 201

# Endpoint: GET /top_publisher
@app.route("/top_publisher", methods=["GET"])
def top_publisher():
    if not articles:
        return jsonify({"message": "No articles available", "top_publisher": None})

    # Count articles for each magazine
    magazine_count = {}
    for article in articles:
        magazine = article["magazine"]
        magazine_count[magazine] = magazine_count.get(magazine, 0) + 1

    # Find the magazine with the most articles
    top_magazine = max(magazine_count, key=magazine_count.get)
    return jsonify({"top_publisher": top_magazine, "article_count": magazine_count[top_magazine]})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
