from flask import Flask, render_template
from .f1anthems import get_anthem_count

app = Flask(__name__)
  
@app.route("/")
def home_view():
        countries = get_anthem_count()
        return render_template("home.html", countries=countries)