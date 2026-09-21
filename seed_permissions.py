from app import app
from models import db, Role, Permission, RolePermission

roles = [
    {
        "name": "admin",
        "description": "Memiliki akses penuh ke sistem."
    },
    {
        "name": "staff",
        "description": "Dapat mengelola data operasional."
    },
    {
        "name": "viewer",
        "description": "Hanya dapat melihat data."
    }
]

permissions = [
    ("dashboard.view", "Melihat dashboard"),
    ("product.view", "Melihat produk"),
    ("product.create", "Menambah produk"),
    ("product.edit", "Mengubah produk"),
    ("product.delete", "Menghapus produk"),
    ("category.view", "Melihat kategori"),
    ("category.create", "Menambah kategori"),
    ("category.edit", "Mengubah kategori"),
    ("category.delete", "Menghapus kategori"),
    ("sale.view", "Melihat transaksi"),
    ("sale.create", "Menambah transaksi"),
    ("user.view", "Melihat pengguna"),
    ("user.create", "Menambah pengguna"),
    ("user.edit", "Mengubah pengguna"),
    ("user.delete", "Menghapus pengguna"),
    ("user.manage", "Mengelola pengguna")
]

with app.app_context():

    # =========================
    # SEED ROLE
    # =========================

    role_objects = {}
    for role_data in roles:
        role = Role.query.filter_by(
            name=role_data["name"]
        ).first()
        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )

            db.session.add(role)
        role_objects[role_data["name"]] = role
    db.session.flush()

    # =========================
    # SEED PERMISSION
    # =========================

    permission_objects = {}
    for name, description in permissions:
        permission = Permission.query.filter_by(
            name=name
        ).first()
        if not permission:
            permission = Permission(
                name=name,
                description=description
            )

            db.session.add(permission)
        permission_objects[name] = permission
    db.session.flush()

    # =========================
    # ROLE PERMISSION
    # =========================

    admin_permissions = [
        permission[0]
        for permission in permissions
    ]

    staff_permissions = [
        "dashboard.view",
        "product.view",
        "product.create",
        "product.edit",
        "category.view",
        "category.create",
        "category.edit",
        "sale.view",
        "sale.create"
    ]

    viewer_permissions = [
        "dashboard.view",
        "product.view",
        "category.view",
        "sale.view"
    ]

    role_permission_map = {
        "admin": admin_permissions,
        "staff": staff_permissions,
        "viewer": viewer_permissions
    }

    for role_name, permission_names in role_permission_map.items():

        role = role_objects[role_name]

        for permission_name in permission_names:

            permission = permission_objects[permission_name]

            existing = RolePermission.query.filter_by(
                role_id=role.id,
                permission_id=permission.id
            ).first()

            if not existing:
                db.session.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id
                    )
                )
    db.session.commit()
    print("Role dan permission berhasil di-seed.")