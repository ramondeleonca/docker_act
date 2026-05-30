import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:demo@db:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/matches", methods=["GET", "POST"])
def matches():
    if request.method == "POST":
        team1 = request.form["team1"].strip()
        team2 = request.form["team2"].strip()
        date = request.form["date"]
        if team1 and team2 and date:
            db.session.add(Match(team1=team1, team2=team2, date=date))
            db.session.commit()
        return redirect(url_for("matches"))

    all_matches = Match.query.order_by(Match.date).all()
    return render_template("matches.html", matches=all_matches)


app.run(host="0.0.0.0", port=5000)
