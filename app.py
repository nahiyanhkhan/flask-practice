from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def homepage():
    return "Welcome to Homepage using Flask!"


@app.route("/hi")
@app.route("/hello")
def hello():
    return "Hello, World!"


@app.route("/user")
@app.route("/user/<name>")
def user(name="Guest"):
    return f"Hello, {name.capitalize()}!"


@app.route("/posts/<int:post_id>/comments/<int:comment_id>")
def posts(post_id, comment_id):
    return f"Post ID: {post_id}, Comment ID: {comment_id}"


@app.route("/welcome")
def welcome():
    data1 = {"name": "John", "age": 30}
    data2 = {"name": "Alice", "age": 25}
    languages = ["Python", "Java", "C++"]
    return render_template("index.html", data1=data1, data2=data2, languages=languages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin":
            error = False
            return render_template("login.html", username=username, error=error)
        else:
            error = True
            return render_template("login.html", error=error)
    return render_template("login.html")


@app.route("/api/countries")
def countries():
    countries_capitals = {
        "Bangladesh": "Dhaka",
        "Sri Lanka": "Sri Jayawardenepura Kotte",
        "Japan": "Tokyo",
        "Saudi Arabia": "Riyadh",
        "Palestine": "East Jerusalem",
    }
    return jsonify(countries_capitals)


@app.route("/api/posts")
def api_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    return jsonify(response.json())


@app.route("/api/posts/<int:post_id>")
def api_post(post_id):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    # return jsonify(response.json()["title"])
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True)
