from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_user_tok
import json
mod = Blueprint('menu', __name__)


@mod.route('/')
def index():
    if not hasattr(g, 'logged_in'):
        g.logged_in = False
    if g.logged_in:
        result=do_get_user_tok(request.cookies)
        user = json.loads(result.response.content)
        flag = user['admin']
        return render_template("index.html",flag=flag)
    else:
        return redirect(url_for('users.login'))