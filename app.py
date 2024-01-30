import os
from flask import Flask, request, session, url_for, redirect, render_template, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy


from markupsafe import escape


app = Flask(__name__)

app.config['SECRET_KEY'] = "0171dd6b0a7be73ac0dd6e78cce68587686c52bf239b888c09440527d4a3906c"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://testdb_8m9n_user:NyFdp6l1O1zi9TvuN3ZTXPj2eZq9Nf27@dpg-cmntgtun7f5s73d0sfr0-a.frankfurt-postgres.render.com/testdb_8m9n"


db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)


from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      user = User.query.filter_by(username=username).first()
      if user and user.check_password(password):
          session['username'] = request.form['username']
          return redirect(url_for('welcome'))
      else:
          return "Invalid username/password combination"
   return render_template('login.html')
#The application also contains a logout () view function that pops up the 'username' session variable.Therefore, the ' /' URL displays the start page again.


#Test route for name parameter
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route("/welcome")
def welcome():
    welcomeText = "<p> Welcome to the gadamn app </p> \n <div> <a href='/'> Home </a> </div>"
    if 'username' in session:
        welcomeText = welcomeText + "<div> <p> You are logged in as " + session['username'] + "</p> </div>"
        return welcomeText
    else:
        #This method is to test compatibility of the template engine with the flask app.
        return '''
                <h1>You are not logged in</h1>
                <div>
                    <a href = "{{url_for('login')}}"> Login </a>
                </div>'''
    
@app.route("/me")
def me_api():
    user = get_current_user()
    if(user == None):
        return {
            "error": "Not logged in"
        }
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    users = users.get("results")
    return [user.to_json() for user in users]

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


def cositasError(error):
    resp = make_response(render_template('test.html'), 501)


def get_current_user():
    return session.get("user", None)

def get_all_users():
    return {"results": users}

if __name__ == "__main__":
    app.run(debug=True)
    
with app.app_context():
    db.create_all()