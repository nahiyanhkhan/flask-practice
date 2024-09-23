from flask import Flask, request, render_template, jsonify
import requests
from models import db, Contact

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def homepage():
    contacts = Contact.query.all()
    return render_template("home.html", contacts=contacts)


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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
