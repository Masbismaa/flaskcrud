from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import db, Category

category_bp = Blueprint(
    "category",
    __name__,
    url_prefix ="/categories"
)

@category_bp.route("/")
def index():
    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "categories/index.html",
        categories = categories
    )

@category_bp.route("/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(
            name = name
        )

        db.session.add(category)
        db.session.commit()

        return redirect(
            url_for("category.index")
        )
    return render_template(
        "categories/add.html"
    )

@category_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        category.name = request.form["name"]

        db.session.commit()

        return redirect(
            url_for("categories.index")
        )
    return render_template(
        "categories/edit.html",
        category=category
    )

@category_bp.route(
    "/delete/<int:id>", methods=["POST"]
)
def delete_category(id):
    category = Category.query.get_or_404(id)

    if category.products:

        flash(
            "Kategori tidak dapat dihapus karena masih memiliki produk!"
        )

        return redirect(
            url_for("category.index")
        )

    db.session.delete(category)
    db.session.commit()

    flash(
        "Kategori berhasil dihapus."
    )

    return redirect(
        url_for("category.index")
    )