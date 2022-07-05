from datetime import datetime
import numpy as np
import pandas as pd

from feature_engineering_example import feature_engineering


# I didn't have time to finish this properly.
def test_feature_engineering():

    historical_orders_df = pd.DataFrame(
        {
            "product_id": [0, 0, 1, 3, 4],
            "customer_id": [0, 0, 0, 1, 1],
            "product_category": ["charm", "charm", "bracelet", None, None],
            "order_id": [0, 1, 1, 2, 2],
            "order_date": [
                datetime(2017, 2, 1),
                datetime(2017, 2, 1),
                datetime(2017, 2, 2),
                datetime(2017, 2, 1),
                datetime(2017, 2, 1),
            ],
        }
    )

    actual_df = feature_engineering.generate_customer_features(
        historical_orders_df, product_categories_for_one_hot=["charm", "bracelet", "ring"]
    )

    assert (actual_df.query("customer_id==0")["prev_charm_count"].values == np.array([0, 1])).all()
    assert (
        actual_df.query("customer_id==0")["this_order_charm_count"].values == np.array([1, 1])
    ).all()
