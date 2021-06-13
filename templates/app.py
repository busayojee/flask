from flask import Flask, render_template, request, redirect, session,logging,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class new(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirm = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'new' + str(self.id)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    def __repr__(self):
        return 'Blog post' + str(self.id)



all_posts=[
        {
        'title': 'Post 1',
        'content': 'this is something in post 1',
        'author': 'Busayo'
    },
    {
        'title': 'Post 2',
        'content': 'this is something in post 2'
    }
]
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            new_member = new(name=name, username=username, password=generate_password_hash(password, method='sha256'), confirm=generate_password_hash(password, method='sha256'))
            db.session.add(new_member)
            db.session.commit()
            flash("You are signed up and can now log in","success")
            return redirect('/login')
        else:
            flash("password does not match with confirm password", "danger")
            return render_template('signup.html')
    return render_template('signup.html')

@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = new.query.filter_by(username=username).first()
        if not user and not check_password_hash(user.password,password):
            flash("please check your login info and try again")
            return render_template('login.html')
        login_user(user)
        return redirect('/')
      
            

    return render_template('login.html')

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/home')
def mainhome():
    return render_template("home.html")
@app.route('/posts', methods=['GET','POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all() 

    return render_template("posts.html",posts=all_posts)

@app.route('/allposts', methods=['GET','POST'])
def allposts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/allposts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all() 

    return render_template("allposts.html",posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.secret_key = "1234567busayoalabi"
    app.run(debug=True)