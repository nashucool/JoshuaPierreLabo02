"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""

    r = get_redis_conn()

    # récupérer les clés order:*
    order_keys = r.keys("order:*")

    orders = []

    for key in order_keys[:limit]:

        # récupérer les données de la commande
        order = r.hgetall(key)

        orders.append(order)

    return orders

from collections import defaultdict

def get_highest_spending_users():
    """Get report of highest spending users"""

    r = get_redis_conn()

    # récupérer toutes les commandes
    order_keys = r.keys("order:*")

    expenses_by_user = defaultdict(float)

    for key in order_keys:

        order = r.hgetall(key)
        print(f"Order data from Redis: {order}")

        user_id = order.get("user_id")
        total_amount = float(order.get("total_amount", 0))

        expenses_by_user[user_id] += total_amount

    # tri décroissant
    highest_spending_users = sorted(
        expenses_by_user.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # top 10
    return highest_spending_users[:10]

def get_best_sellers():
    """Get report of best selling products"""

    r = get_redis_conn()

    product_keys = r.keys("product:*")

    best_sellers = []

    for key in product_keys:

        quantity_sold = int(r.get(key))

        product_id = key.split(":")[1]

        best_sellers.append((product_id, quantity_sold))

    best_sellers = sorted(
        best_sellers,
        key=lambda x: x[1],
        reverse=True
    )

    return best_sellers