import os.path
import platform
from flask import Flask, render_template, request, redirect, session, flash
from models import db, User
app = Flask(__name__)


@app.route("/")
def hello():
    if 'username' not in session:
        return redirect('/login/')
    else:
        username = session['username']
        return render_template("index.html")

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("사용자 이름이나 비밀번호가 입력되지 않았습니다.")
            return render_template("signup.html")
        else:
            usertable = User()
            usertable.username = username
            usertable.password = password

            db.session.add(usertable)
            db.session.commit()

            flash("회원가입이 정상적으로 처리되었습니다.")
            return redirect('/')
    else:
        return render_template("signup.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("입력되지 않은 정보가 있습니다.")
            return render_template("login.html")
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    session['username'] = username
                    return redirect('/')
                else:
                    flash("비밀번호가 다릅니다.")
                    return render_template("login.html")
            else:
                flash("사용자가 존재하지 않습니다.")
                return render_template("login.html")
    else:
        return render_template("login.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(400)
def page_not_found(error):
    return render_template('404.html')


if __name__ == "__main__":
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        dbfile = os.path.join(basedir, 'private', 'db.sqlite')
        print(dbfile)
        app.config['SECRET_KEY'] = 'ICEWALL'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.app = app
        db.create_all()

        with open(os.path.join(basedir, 'private', 'IP')) as file_data:
            hostIP = file_data.read()
            print(hostIP)

        #checking platform
        if "aws"in platform.platform():
            with open(os.path.join(basedir, 'private', 'IP')) as file_data:
                host_IP, host_port = file_data.read().split()
            app.run(host=host_IP, port=host_port, debug=True)
        else:
            app.run(port=5000, debug=True)
