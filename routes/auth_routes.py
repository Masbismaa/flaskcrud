import secrets

from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from datetime import datetime, timedelta
from models import User, PasswordResetOTP, db

from werkzeug.security import generate_password_hash, check_password_hash

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

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        phone = request.form.get("phone")

        if not email and not phone:
            flash("Masukkan email atau nomor WhatsApp.")
            return redirect(url_for("auth.forgot_password"))

        user = None

        if email:
            user = User.query.filter_by(email=email).first()

        if not user and phone:
            user = User.query.filter_by(phone=phone).first()

        if not user:
            flash("Akun tidak ditemukan.")
            return redirect(url_for("auth.forgot_password"))

        if not user.is_active:
            flash("Akun sedang dinonaktifkan.")
            return redirect(url_for("auth.forgot_password"))

        # Generate OTP 6 digit
        otp = f"{secrets.randbelow(1000000):06d}"

        # Hash OTP sebelum disimpan ke database
        otp_hash = generate_password_hash(otp)

        # OTP berlaku selama 5 menit
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        password_reset_otp = PasswordResetOTP(
            user_id=user.id,
            otp_hash=otp_hash,
            expires_at=expires_at
        )

        db.session.add(password_reset_otp)
        db.session.commit()

        # Untuk development saja.
        # Nanti diganti dengan pengiriman Email/WhatsApp.
        print(f"OTP untuk {user.email}: {otp}")
        session["reset_user_id"]=user.id

        flash("OTP berhasil dibuat. Silahan masukkan OTP.")
        return redirect(url_for("auth.verify_otp"))
    return render_template("forgot_password.html")

@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    user_id = session.get("reset_user_id")

    if not user_id:
        flash("Silakan mulai proses lupa password terlebih dahulu.")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        otp = request.form.get("otp")

        if not otp:
            flash("OTP wajib diisi.")
            return redirect(url_for("auth.verify_otp"))

        password_reset_otp = PasswordResetOTP.query.filter_by(
            user_id=user.id,
            used_at=None
        ).order_by(
            PasswordResetOTP.id.desc()
        ).first()

        if not password_reset_otp:
            flash("OTP tidak ditemukan atau sudah digunakan.")
            return redirect(url_for("auth.forgot_password"))

        if datetime.utcnow() > password_reset_otp.expires_at:
            flash("OTP sudah kedaluwarsa. Silakan minta OTP baru.")
            return redirect(url_for("auth.forgot_password"))

        if not check_password_hash(
            password_reset_otp.otp_hash,
            otp
        ):
            flash("OTP salah.")
            return redirect(url_for("auth.verify_otp"))

        password_reset_otp.used_at = datetime.utcnow()

        db.session.commit()

        session["reset_verified"] = True

        flash("OTP berhasil diverifikasi.")
        return redirect(url_for("auth.reset_password"))
    return render_template(
        "verify_otp.html",
        user=user
    )

@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    user_id = session.get("reset_user_id")
    reset_verified = session.get("reset_verified")

    if not user_id or not reset_verified:
        flash("Silakan lakukan verifikasi OTP terlebih dahulu.")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or not confirm_password:
            flash("Password baru dan konfirmasi wajib diisi.")
            return redirect(url_for("auth.reset_password"))

        if new_password != confirm_password:
            flash("Konfirmasi password tidak cocok.")
            return redirect(url_for("auth.reset_password"))

        user.set_password(new_password)

        db.session.commit()

        session.pop("reset_user_id", None)
        session.pop("reset_verified", None)

        flash("Password berhasil direset. Silakan login.")
        return redirect(url_for("auth.login"))

    return render_template(
        "reset_password.html",
        user=user
    )

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    session.pop("user_name", None)

    flash("Berhasil Logout")

    return redirect(
        url_for("auth.login")
    )
