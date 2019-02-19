from gui.views import meh, fix, car, user, menu
import flask
from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort


from gui.config import current_config

app = flask.Flask(__name__)


@app.before_request
def load_current_user():
    if 'token' in request.cookies:
        g.logged_in = True
        g.user = request.cookies
    else:
        g.user = None
        g.logged_in = False

app.config.from_object(current_config)
app.register_blueprint(meh.mod)
app.register_blueprint(fix.mod)
app.register_blueprint(car.mod)
app.register_blueprint(user.mod)
app.register_blueprint(menu.mod)

if __name__ == '__main__':
    app.run(port=5005)