from functools import wraps

from flask import(
    session,
    redirect,
    url_for,
    flash,
    abort
)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Silahkan login terlebih dahulu!")
            return redirect(
                url_for("auth.login")
            )
        return view(*args, **kwargs)
    return wrapped_view

def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                flash("Silahkan login terlebih dahulu!")
                return redirect(
                    url_for('auth.login')
                )
            user_role = session.get("user_role")
            if user_role not in allowed_roles: 
                abort(403)
            return view(*args,**kwargs)
        return wrapped_view
    return decorator