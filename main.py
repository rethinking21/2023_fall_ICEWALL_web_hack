import os.path
import platform
from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import db, User, Post, Comment
app = Flask(__name__)


@app.route("/")
def hello():
    if 'username' not in session:
        return redirect('/login/')
    else:
        username = session['username']
        return render_template("index.html", user_name=username)
    
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("사용자 이름이나 비밀번호가 입력되지 않았습니다.")
            return render_template("signup.html")
        elif username == 'null':
            flash("사용자 이름이 적절하지 않습니다.")
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

@app.route('/getsessiondata/<key>')
def get_session_data(key):
    try:
        res = session[key]
    except KeyError:
        return 'null'
    else:
        return res

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

@app.route("/logout/")
def logout():
    if 'username' not in session:
        flash("정상적인 요청이 아닙니다.")
    else:
        session.pop('username', None)
    return redirect('/')

@app.route('/post/', methods=['GET', 'POST'])
def post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')

        if not(title and content):
            return "입력되지 않은 정보가 있습니다."
        else:
            posttable = Post()
            posttable.title = title
            posttable.content = content

            db.session.add(posttable)
            db.session.commit()
            return redirect('/post_list')
    else:
        return render_template('post.html')
            

@app.route('/post_list/', methods=['GET', 'POST'])
def post_list():
    post_list = Post.query.order_by(Post.datetime.asc())
    return render_template("post_list.html", post_list=post_list)

@app.route('/detail/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post_list/')

@app.route('/detail/<int:post_id>/comment/', methods=['GET', 'POST'])
def comment(post_id):
    if request.method == "POST":
        content = request.form.get('content')

        post = Post.query.get_or_404(post_id)
        comment = Comment()
        comment.content = content
        comment.post = post
        comment.post_id = post_id
        
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('detail', post_id=post_id))
    else:
        return render_template("comment.html")


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