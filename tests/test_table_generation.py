import pandas as pd
import pandera as pa
import pytest

from feature_engineering_example import table_generation


@pytest.fixture()
def product_categories():
    return ["ring", "bracelet", "charm", None]


def test_generate_products_table(product_categories):
    n_products = 100
    actual_df = table_generation.generate_products_table(n_products, product_categories)

    expected_schema = pa.DataFrameSchema(
        {
            "product_id": pa.Column(int, checks=pa.Check.le(n_products)),
            "product_category": pa.Column(
                object, checks=pa.Check.isin(product_categories), nullable=True
            ),
        }
    )

    expected_schema.validate(actual_df)


def test_historical_orders_table():
    n_customers = 2
    n_orders = 6
    max_products_per_order = 10
    max_product_id = 2
    product_categories = ["ring", "bracelet", None]

    products_df = pd.DataFrame(
        {"product_id": range(max_product_id + 1), "product_category": product_categories}
    )

    actual_df = table_generation.generate_historical_orders_table(
        products_df, n_customers, n_orders, max_products_per_order
    )

    expected_schema = pa.DataFrameSchema(
        {
            "product_id": pa.Column(int, checks=pa.Check.le(max_product_id)),
            "product_category": pa.Column(
                object, checks=pa.Check.isin(product_categories), nullable=True
            ),
            "customer_id": pa.Column(int, checks=pa.Check.le(n_customers)),
            "order_id": pa.Column(int, checks=pa.Check.le(n_orders)),
            "order_date": pa.Column(pa.dtypes.DateTime),
        }
    )

    expected_schema.validate(actual_df)
