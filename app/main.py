from flask import Flask, render_template
from .f1anthems import get_anthem_count, get_race_count

app = Flask(__name__)
  
@app.route("/")
def home_view():
        countries = get_anthem_count()
        race_count = get_race_count()
        return render_template("home.html", race_count=race_count, countries=countries)