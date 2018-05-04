"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import Game, connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    session['RSVP'] = True
    flash("Yay!")
    return redirect("/")


@app.route("/games")
def games():

    try:
        if session['RSVP'] is True:
            games = Game.query.all()
            return render_template("games.html", games=games)
    except:
        return redirect("/")

@app.route("/add_game", methods=['POST'])
def add_game():
    """ Add a game to the list that you plan to bring to the party """

    # For some reason these arguments are being read as "Null", either when
    # coming in from the POST request, or when getting passed to SQL
    game_name = request.form.get('gameName')
    game_desc = request.form.get('gameDesc')

    db.session.add(Game(name=game_name, description=game_desc))
    db.session.commit()

    all_games_list = db.session.query(games).all()

    return all_games_list


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
