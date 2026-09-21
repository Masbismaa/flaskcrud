from functools import wraps

from flask import(
    session,
    redirect,
    url_for,
    flash,
    abort
)

from models import User, Role, Permission, RolePermission

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

def has_permission(permission_name):
    user_id = session.get("user_id")

    if not user_id:
        return False

    user = User.query.get(user_id)

    if not user:
        return False

    role = Role.query.filter_by(
        name=user.role
    ).first()

    if not role:
        return False

    permission = Permission.query.filter_by(
        name=permission_name
    ).first()

    if not permission:
        return False

    role_permission = RolePermission.query.filter_by(
        role_id=role.id,
        permission_id=permission.id
    ).first()

    return role_permission is not None

def permission_required(permission_name):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if "user_id" not in session:
                flash("Silahkan login terlebih dahulu.")
                return redirect(
                    url_for("auth.login")
                )

            if not has_permission(permission_name):
                abort(403)

            return view(*args, **kwargs)

        return wrapped_view

    return decorator