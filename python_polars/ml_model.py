import polars as pl
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


order_reviews_ds = pl.read_csv("olist_order_reviews_dataset.csv", try_parse_dates=True)
order_items_ds = pl.read_csv("olist_order_items_dataset.csv", try_parse_dates=True)
order_payments_ds = pl.read_csv("olist_order_payments_dataset.csv", try_parse_dates=True)
total_ds = order_reviews_ds.join(order_items_ds, on = "order_id").join(order_payments_ds, on = "order_id")
result = total_ds.select(
    pl.col("price"),
    pl.col("freight_value"),
    pl.col("payment_value"),
    pl.col("review_score")
).drop_nulls()
X = result.drop("review_score").to_numpy()
y = result["review_score"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
model = LogisticRegression(max_iter = 500)
model.fit(X_train, y_train)
joblib.dump(model, "review_model.pkl")
