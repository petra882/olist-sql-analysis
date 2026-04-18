import polars as pl
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


order_reviews_ds = pl.read_csv("olist_order_reviews_dataset.csv", try_parse_dates=True)
order_items_ds = pl.read_csv("olist_order_items_dataset.csv", try_parse_dates=True)
order_payments_ds = pl.read_csv("olist_order_payments_dataset.csv", try_parse_dates=True)
orders_ds = pl.read_csv("olist_orders_dataset.csv", try_parse_dates=True)
sellers_ds = pl.read_csv("olist_sellers_dataset.csv", try_parse_dates=True)
products_ds = pl.read_csv("olist_products_dataset.csv")
total_ds = (order_reviews_ds.join(order_items_ds, on = "order_id").join(order_payments_ds, on = "order_id")
            .join(orders_ds, on = "order_id")).join(sellers_ds, on = "seller_id").join(products_ds, on = "product_id")
result = total_ds.select(
    pl.col("price"),
    pl.col("freight_value"),
    pl.col("payment_value"),
    pl.col("review_score"),
    (pl.col("order_delivered_customer_date") -pl.col("order_purchase_timestamp")).dt.total_days().alias("delivery_time"),
    pl.col("product_category_name"),
    pl.col("seller_state")
).drop_nulls()
result_to_encode = result.select(
    pl.col("product_category_name"),
    pl.col("seller_state")
).to_numpy()
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

X_categorical_encoded = encoder.fit_transform(result_to_encode)

X_numeric = result.drop(["review_score", "product_category_name", "seller_state"]).to_numpy()

y = result["review_score"].to_numpy()

X_final = np.hstack([X_numeric, X_categorical_encoded])

X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(accuracy_score(y_test, y_pred))

joblib.dump(encoder, "D:/projects/e-commercial/fast_api/encoder.pkl")
joblib.dump(model, "D:/projects/e-commercial/fast_api/review_model_v2.pkl")