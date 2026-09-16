from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from models import db, Product, Category, Sale

product_bp = Blueprint(
    "product",
    __name__
)


@product_bp.route("/")
def index():

    products = Product.query.all()

    return render_template(
        "index.html",
        products=products
    )

@product_bp.route("/dashboard")
def dashboard():
    total_products = Product.query.count()
    total_stock = db.session.query(
        db.func.sum(Product.stock)
    ).scalar() or 0

    out_of_stock = Product.query.filter(
        Product.stock == 0
    ).count ()

    low_stock = Product.query.filter(
        Product.stock > 0,
        Product.stock <= 5
    ).order_by(
        Product.stock.asc()
    ).all()

    recent_sales = Sale.query.order_by(
        Sale.created_at.asc()
    ).limit(5).all()

    return render_template(
        "dashboard.html", total_products = total_products,
        total_stock = total_stock, out_of_stock = out_of_stock,
        low_stock = low_stock, recent_sales = recent_sales
    )


@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]

        product = Product(
            name=name,
            price=price,
            stock=stock,
            category_id=category_id
        )

        db.session.add(product)
        db.session.commit()

        return redirect(
            url_for("product.index")
        )
    return render_template(
        "add.html",
        categories=categories
    )


@product_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.price = request.form["price"]
        product.stock = request.form["stock"]
        product.category_id = request.form["category"]

        db.session.commit()

        return redirect(
            url_for("product.index")
        )

    categories = Category.query.all()

    return render_template(
        "edit.html",
        product=product,
        categories=categories
    )


@product_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(
        url_for("product.index")
    )