from flask import(
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session
)

from models import User, db

from utils.auth import role_required

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/users"
)

@user_bp.route("/")
@role_required("admin")
def index():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("users/index.html", users=users)

@user_bp.route("/add", methods=["GET", "POST"])
@role_required("admin")
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not name or not email or not password or not role:
            flash("Semua field wajib diisi!")
            return redirect(url_for("user.add_user"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email sudah digunakan.")
            return redirect(url_for("user.add_user"))

        user = User(
            name = name,
            email = email,
            role = role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User berhasil dibuat.")
        return redirect(url_for("user.index"))
    return render_template("users/add.html")

@user_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")

        if not name or not email or not role:
            flash("Name, Email, dan Role wajib diisi!")
            return redirect(
                url_for("user.edit_user", id=id),
            )

        user.name = name
        user.email = email
        user.role = role

        db.session.commit()

        flash("Data User berhasil di Update!")
        return redirect(url_for("user.index"))
    return render_template("users/edit.html", user=user)

@user_bp.route("/change-password/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def change_password(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or not confirm_password:
            flash("Password wajib diisi!.")
            return redirect(
                url_for("user.change_password", id=id)
            )

        user.set_password(password)
        db.session.commit()

        flash("Password user berhasil diubah.")
        return redirect(
            url_for("user.index")
        )
    return render_template(
        "users/change_password.html",
        user=user
    )

@user_bp.route("/toggle-status/<int:id>", methods=["POST"])
@role_required("admin")
def toggle_status(id):
    user = User.query.get_or_404(id)

    if user.id == session.get("user_id"):
        flash("Kamu tidak dapat menonaktifkan akun sendiri.")
        return redirect(url_for("user.index"))

    user.is_active = not user.is_active

    db.session.commit()

    if user.is_active:
        flash("User berhasil diaktifkan.")
    else:
        flash("User berhasil dinonaktifkan.")

    return redirect(url_for("user.index"))