from flask import Flask
from flask_login import LoginManager
from flask import session
from flask import redirect
from flask import render_template

from markupsafe import escape


app = Flask(__name__)

login_manager = LoginManager()

app.secret_key = '0171dd6b0a7be73ac0dd6e78cce68587686c52bf239b888c09440527d4a3906c'

#secret_key = 0171dd6b0a7be73ac0dd6e78cce68587686c52bf239b888c09440527d4a3906c for key 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf

#postgres://testdb_8m9n_user:NyFdp6l1O1zi9TvuN3ZTXPj2eZq9Nf27@dpg-cmntgtun7f5s73d0sfr0-a.frankfurt-postgres.render.com/testdb_8m9n

def url_for(yea):
    return yea

@app.route("/")
def hello_world():
    return "<p>Gad mf damn </p>"

@app.route("/login", methods = ['GET', 'POST'])
def login():    
    login_manager.init_app(app)
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('welcome'))

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route("/main")
def gadamn():
    return "<p>gadamn</p>"

@app.route("/welcome")
def welcome():
    welcomeText = "<p> Welcome to the gadamn app </p> \n <div> <a href='/'> Home </a> </div>"
    if 'username' in session:
        welcomeText = welcomeText + "<div> <p> You are logged in as " + session['username'] + "</p> </div>"
    else:
        return 'You are not logged in\n' + '<div> <a href="/login"> Login </a> </div>'
    
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]


#@app.errorhandler(404)
#def not_found(error):
#    return render_template('error.html'), 404

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


def cositasError(error):
    resp = make_response(render_template('test.html'), 501)