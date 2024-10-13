from flask import flash, jsonify, redirect, render_template, request, session, url_for

from application import app, db
from application.forms import LoginForm, RegisterForm
from application.models import Course, Enrollment, User


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session["user_id"] = user.id
            session["username"] = user.first_name
            session["is_admin"] = user.is_admin
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session["user_id"] = False
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        is_admin = form.is_admin.data

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/user")
def user():
    users = User.query.all()
    return render_template("user.html", users=users)


@app.route("/api/")
@app.route("/api/<index>")
def api(index=None):
    course_data = (
        Course.query.all()
        if index is None
        else Course.query.get(index).query.get(index)
    )
    return jsonify(course_data)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Winter 2024"
    classes = Course.query.order_by(Course.title).all()
    return render_template("courses.html", course_data=classes, courses=True, term=term)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get("username"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")

    # Query to fetch the courses the user is enrolled in
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    classes = []
    for enrollment in enrollments:
        if course := Course.query.filter_by(id=enrollment.course_id).first():
            classes.append(course)

    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )


@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if not session.get("username") or not session.get("is_admin"):
        flash("You are not authorized to access this page!", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        course_id = request.form.get("course_id")
        title = request.form.get("title")
        description = request.form.get("description")
        credits = request.form.get("credits")
        term = request.form.get("term")

        # Server-side validation for required fields
        if not course_id or not title or not description or not credits or not term:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_course"))

        # Process valid course data
        new_course = Course(
            course_id=course_id,
            title=title,
            description=description,
            credits=credits,
            term=term,
        )
        db.session.add(new_course)
        db.session.commit()
        flash(f"Course {title} added successfully!", "success")
        return redirect(url_for("courses"))
    return render_template("add_course.html", title="Add Course", add_course=True)


@app.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        course.title = request.form["title"]
        course.description = request.form["description"]
        course.credits = request.form["credits"]
        course.term = request.form["term"]

        db.session.commit()
        flash(f"Course {course.title} updated successfully!", "success")
        return redirect(url_for("courses"))

    return render_template("edit_course.html", course=course, title="Edit Course")


@app.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    if not session.get("is_admin"):
        flash("You are not authorized to delete courses!", "danger")
        return redirect(url_for("courses"))

    courses = Course.query.get_or_404(course_id)
    db.session.delete(courses)
    db.session.commit()
    flash(f"Course {courses.title} deleted successfully!", "success")
    return redirect(url_for("courses"))
