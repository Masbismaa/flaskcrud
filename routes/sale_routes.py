from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from models import db, Sale, Product, SaleItem

sale_bp = Blueprint(
    "sale",
    __name__,
    url_prefix="/sales"
)

@sale_bp.route("/")
def index():
    sales = Sale.query.order_by(
        Sale.created_at.desc()
    ).all()

    return render_template(
        "sales/index.html",
        sales=sales
    )

@sale_bp.route("/add", methods=["GET", "POST"])
def add_sale():

    products = Product.query.order_by(
        Product.name.asc()
    ).all()

    if request.method == "POST":

        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity")

        if not product_id or not quantity:
            return "Product ID atau quantity tidak terkirim", 400

        product_id = int(product_id)
        quantity = int(quantity)

        product = Product.query.get_or_404(product_id)

        total = product.price * quantity

        sale = Sale(
            total=total
        )

        db.session.add(sale)

        db.session.flush()

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )

        db.session.add(sale_item)

        db.session.commit()

        return redirect(
            url_for("sale.index")
        )
    return render_template(
        "sales/add.html",
        products=products
    )