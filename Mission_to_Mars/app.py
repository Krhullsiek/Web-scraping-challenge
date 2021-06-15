# Dependencies
from logging import debug
from re import T
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
mongo = PyMongo(app)

# Or set inline
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_info)


@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)