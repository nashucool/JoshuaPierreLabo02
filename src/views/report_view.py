"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from controllers.order_controller import get_report_highest_spending_users, get_report_best_sellers

def show_highest_spending_users():
    """ Show report of highest spending users """

    users = get_report_highest_spending_users()

    users_html = "<ul>"

    for user_id, total in users:
        users_html += f"<li>Utilisateur {user_id}: {total}$</li>"

    users_html += "</ul>"

    return get_template(
        f"<h2>Les plus gros acheteurs</h2><p>{users_html}</p>"
    )

def show_best_sellers():
    """ Show report of best selling products """

    products = get_report_best_sellers()

    html = "<h2>Les articles les plus vendus</h2><p><ul>"

    for product_id, quantity_sold in products:
        html += f"<li>Produit {product_id}: {quantity_sold} vendus</li>"

    html += "</ul></p>"

    return get_template(html)