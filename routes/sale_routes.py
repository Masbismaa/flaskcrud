from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models import db, Sale, Product, SaleItem
from utils.auth import login_required, role_required

sale_bp = Blueprint(
    "sale",
    __name__,
    url_prefix="/sales"
)

def get_cart():
    return session.get("cart", {})

@sale_bp.route("/cart/add", methods=["POST"])
@login_required
@role_required("admin", "staff")
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

    if not product_id or not quantity:
        return "Product ID atau quantity tidak terkirim", 400

    product_id = int(product_id)
    quantity = int(quantity)

    product = Product.query.get_or_404(product_id)

    if quantity <= 0:
        return "Quantity harus lebih dari 0", 400
    if quantity > product.stock:
        return "Stok produk tidak cukup", 400

    cart = get_cart()

    product_key = str(product_id)
    current_quantity = cart.get(
        product_key, 0
    )

    new_quantity = current_quantity + quantity
    if new_quantity > product.stock:
        return "Jumlah produk di keranjang melebihi stok", 400

    cart[product_key] = new_quantity
    session["cart"] = cart
    return redirect(
        url_for("sale.add_sale")
    )

@sale_bp.route("/cart/remove/<int:product_id>")
@login_required
@role_required("admin", "staff")
def remove_from_cart(product_id):
    cart = get_cart()

    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]

    session["cart"] = cart

    return redirect(
        url_for("sale.add_sale")
    )

@sale_bp.route("/")
@login_required
def index():
    sales = Sale.query.order_by(
        Sale.created_at.asc()
    ).all()

    return render_template(
        "sales/index.html",
        sales=sales
    )

@sale_bp.route("/<int:sale_id>")
@login_required
def detail_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    return render_template(
        "sales/detail.html",
        sale = sale
    )

@sale_bp.route("/add")
@login_required
@role_required("admin", "staff")
def add_sale():

    products = Product.query.order_by(
        Product.name.asc()
    ).all()

    cart = get_cart()
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            cart_total += subtotal
    
    return render_template(
        "sales/add.html",
        products=products, cart_items=cart_items, cart_total=cart_total
    )

@sale_bp.route("/checkout", methods=["POST"])
@login_required
@role_required("admin", "staff")
def checkout():
    cart = get_cart()

    if not cart:
        return "Keranjang masih kosong", 400

    cart_total = 0
    cart_products = []

    for product_id, quantity in cart.items():

        product = Product.query.get(int(product_id))

        if not product:
            return "Produk tidak ditemukan", 404

        if quantity <= 0:
            return "Quantity tidak valid", 400

        if quantity > product.stock:
            return f"Stok {product.name} tidak mencukupi", 400

        subtotal = product.price * quantity

        cart_total += subtotal

        cart_products.append({
            "product": product,
            "quantity": quantity
        })

    sale = Sale(
        total=cart_total
    )

    db.session.add(sale)
    db.session.flush()

    for item in cart_products:

        product = item["product"]
        quantity = item["quantity"]

        product.stock -= quantity

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )

        db.session.add(sale_item)

    db.session.commit()

    session.pop("cart", None)

    return redirect(
        url_for(
            "sale.detail_sale",
            sale_id=sale.id
        )
    )

@sale_bp.route("/cart/clear")
@login_required
@role_required("admin", "staff")
def clear_cart():
    session.pop("cart", None)
    return redirect(
        url_for("sale.add_sale")
    )