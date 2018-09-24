from flask import render_template, url_for, flash, redirect, request
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, BlogPostForm, UpdatePostForm
from flask_blog.models import User, Post
from flask_blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("home.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html", title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title='register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # inorder to redirect to the intended page if logs in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email or password", "danger")
    return render_template("login.html", title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=current_user.image)
    return render_template('account.html', title='Accoont', image_file=image_file, form=form)


@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    image_file = url_for('static', filename=current_user.image)
    form = BlogPostForm()
    posts = current_user.posts
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('blog.html', title="Blog", form=form, posts=posts, image_file=image_file)


@app.route('/remove/<post_id>')
@login_required
def remove_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post.user_id == current_user.id:
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        return redirect(url_for('blog'))
    else:
        flash("post cannot be deleted", "danger")
    return redirect(url_for('blog'))

@app.route('/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdatePostForm()
    if post.author == current_user and form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('blog'))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("blog.html", form=form, title="update post")
