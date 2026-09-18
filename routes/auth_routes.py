from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import User

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix = "/auth"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email dan password wajib diisi!")
            return redirect(
                url_for("auth.login")
            )

        user = User.query.filter_by(
            email = email
        ).first()

        if not user or not user.check_password(password):
            flash("Email atau password anda salah!")
            return redirect(
                url_for("auth.login")
            )

        if not user.is_active:
            flash("Akun kamu sedang dinonaktifkan, Hubungi admin!")
            return redirect(
                url_for("auth.login")
            )

        session["user_id"] = user.id
        session["user_role"] = user.role
        session["user_name"] = user.name

        flash("Login Berhasil")
        return redirect(
            url_for("product.dashboard")
        )
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    session.pop("user_name", None)

    flash("Berhasil Logout")

    return redirect(
        url_for("auth.login")
    )
