import numpy as np
import pandas as pd


def _previous_customer_category_purchases(dfg, category_purchase_columns):
    for col in category_purchase_columns:
        in_total_bought = np.cumsum(dfg[col].values)
        previously_bought = in_total_bought - dfg[col].values
        dfg[f"prev_{col}_count"] = previously_bought

    return dfg


def _this_order_category_purchased(historical_orders_df, one_hot_cols):
    historical_orders_df = historical_orders_df.sort_values("order_date")
    purchase_category_counts_df = historical_orders_df.groupby(["customer_id", "order_id"])[
        one_hot_cols
    ].sum()  # .rename({column: f"this_order_{column}_count" for column in one_hot_cols}, axis=1).reset_index()
    historical_orders_df = historical_orders_df.drop(one_hot_cols, axis=1)
    df = historical_orders_df.merge(
        purchase_category_counts_df, on=["customer_id", "order_id"], how="left"
    )
    df = df.drop_duplicates(subset=["customer_id", "order_id"])
    return df


def generate_customer_features(historical_orders_df: pd.DataFrame, product_categories_for_one_hot):
    categorical_one_hot_encoding_df = pd.get_dummies(historical_orders_df["product_category"])
    non_existing_categories = set(product_categories_for_one_hot).difference(
        set(categorical_one_hot_encoding_df.columns.values)
    )
    for col in non_existing_categories:
        categorical_one_hot_encoding_df[col] = 0
    historical_orders_df = pd.concat(
        [historical_orders_df, categorical_one_hot_encoding_df], axis=1
    )

    df = _this_order_category_purchased(historical_orders_df, product_categories_for_one_hot)

    df = df.groupby("customer_id").apply(
        lambda dfg: _previous_customer_category_purchases(dfg, product_categories_for_one_hot)
    )
    df = df.rename(
        {column: f"this_order_{column}_count" for column in product_categories_for_one_hot}, axis=1
    ).reset_index()
    df = df.drop("index", axis=1)
    return df
