import os
from pathlib import Path
from typing import List

import typer
from feature_engineering import generate_customer_features
from table_generation import generate_historical_orders_table, generate_products_table

app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command()
def main(
    n_customers: int = typer.Option(default=20, envvar="N_CUSTOMERS"),
    n_products: int = typer.Option(default=20, envvar="N_PRODUCTS"),
    product_categories: List[str] = typer.Option(default=["charm", "bracelet", "ring"]),
    save_path: str = typer.Option(default="output"),
    n_orders: int = typer.Option(default=1000, envvar="N_ORDERS"),
    max_products_per_order: int = typer.Option(default=10),
):
    product_categories = list(product_categories)
    products_table_df = generate_products_table(n_products, product_categories)
    historical_table_df = generate_historical_orders_table(
        products_table_df, n_customers, n_orders, max_products_per_order
    )
    customer_features_df = generate_customer_features(historical_table_df, product_categories)

    save_path = Path(save_path, exists=True)
    products_table_df.to_csv(save_path.joinpath("products.csv"))
    historical_table_df.to_csv(save_path.joinpath("historical_orders.csv"))
    customer_features_df.to_csv(save_path.joinpath("customer_features.csv"))


if __name__ == "__main__":
    app()
