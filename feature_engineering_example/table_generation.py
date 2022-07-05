import datetime
from copy import copy
from typing import List

import numpy as np
import pandas as pd

from feature_engineering_example.utils import rng


def generate_products_table(n_products: int, product_categories: List[str]) -> pd.DataFrame:
    """Randomly generates products table. Adds None as a category.

    Args:
        n_products (int): Number of products to add to the table
        product_categories (List): Categories the products can have.

    Returns:
        pd.DataFrame: Product table with columns: product_id, product_category
    """
    product_categories = copy(product_categories)  # Remove reference
    product_categories.append(None)
    random_category_indices = rng().randint(low=0, high=len(product_categories), size=n_products)
    ids = range(n_products)
    categories = np.array(product_categories)[random_category_indices]
    df = pd.DataFrame({"product_id": ids, "product_category": categories})
    return df


def _generate_order(
    products_df: pd.DataFrame,
    start_date,
    n_days_period_length,
    n_customers,
    max_products_per_order,
    random_gen,
):
    order_date = start_date + datetime.timedelta(
        days=random_gen.randint(low=0, high=n_days_period_length)
    )
    customer_id = random_gen.randint(low=0, high=n_customers)

    n_products_purchased = random_gen.randint(low=1, high=max_products_per_order)
    products_purchased = random_gen.randint(low=0, high=len(products_df), size=n_products_purchased)

    order_df = products_df.iloc[products_purchased].copy()
    order_df["customer_id"] = customer_id
    order_df["order_date"] = order_date
    return order_df


def generate_historical_orders_table(
    products_df: pd.DataFrame, n_customers: int, n_orders: int, max_products_per_order: int = 10
) -> pd.DataFrame:
    """Randomly generates a historical orders table.

    Args:
        products_df (pd.DataFrame): Products table.
        n_costumers (int): Number of customers creating orders.
        n_orders (int):
        min_products_per_order (int, optional): _description_. Defaults to 1.
        max_products_per_order (int, optional): _description_. Defaults to 10.

    Returns:
        pd.DataFrame: _description_
    """
    start_date = datetime.datetime(2017, 1, 1)
    n_days_period_length = 100
    historical_orders_list = list()
    random_gen = rng()
    for order_id in range(n_orders):
        order_df = _generate_order(
            products_df,
            start_date,
            n_days_period_length,
            n_customers,
            max_products_per_order,
            random_gen,
        )
        order_df["order_id"] = order_id
        historical_orders_list.append(order_df)

    return pd.concat(historical_orders_list)
