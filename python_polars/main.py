import polars as pl
import datetime as dt

"""
Olist Brazilian E-Commerce: Polars Analysis
============================================
Перенос SQL-запросов из projsql.sql на Polars.
Автор: Артеменко Пётр
Дата: 13.04.2026
"""


"""
-- Помесячная динамика заказов:
orders_dataset = pl.read_csv('olist_orders_dataset.csv', try_parse_dates=True)

result = orders_dataset.select(
    pl.col("order_purchase_timestamp").dt.month().alias("month"),
    pl.col("order_id").alias("count")
).group_by("month").agg(pl.col("count").count()).sort("month")
"""

"""
-- Топ-10 категорий по объему продаж
products_ds = pl.read_csv('olist_products_dataset.csv', try_parse_dates=True)
order_items_ds = pl.read_csv('olist_order_items_dataset.csv', try_parse_dates=True)
total_ds = products_ds.join(order_items_ds, on='product_id')
result = total_ds.select(
    pl.col("product_category_name"),
    pl.col("price"),
).group_by("product_category_name").agg(pl.col("price").alias("avenue").sum()).sort("avenue", descending=True).limit(10)
"""

"""
-- Города с высокой оценкой
customers_ds = pl.read_csv('olist_customers_dataset.csv', try_parse_dates=True)
orders_ds = pl.read_csv('olist_orders_dataset.csv', try_parse_dates=True)
order_review_ds = pl.read_csv('olist_order_reviews_dataset.csv', try_parse_dates=True)
total_ds = customers_ds.join(orders_ds, on='customer_id').join(order_review_ds, on='order_id')
result = (total_ds.select(
    pl.col("customer_city"),
    pl.col("review_score")
).
          filter(pl.col("review_score") == 5).group_by("customer_city").agg(pl.col("customer_city").count().alias("count_5")).
          sort("count_5", descending=True).limit(5))
"""

"""
--среднее время доставки по штатам
orders_ds = pl.read_csv('olist_orders_dataset.csv', try_parse_dates=True)
customers_ds = pl.read_csv("olist_customers_dataset.csv", try_parse_dates=True)
total_ds = orders_ds.join(customers_ds, on='customer_id')
result = (total_ds.select(
    pl.col("customer_state"),
    pl.col("order_status"),
    (pl.col("order_delivered_customer_date") - pl.col("order_approved_at")).alias("det"),
    pl.col("order_approved_at"),
    pl.col("order_delivered_customer_date")
).filter(pl.col("order_status") == "delivered", pl.col("order_approved_at").is_not_null(),
         pl.col("order_delivered_customer_date").is_not_null()).
          group_by("customer_state").agg(pl.col("det").mean().alias("avg"))).sort("avg", descending=True)
"""

"""
--клиенты совершившие только один заказ
order_ds = pl.read_csv('olist_orders_dataset.csv', try_parse_dates=True)
customers_ds = pl.read_csv("olist_customers_dataset.csv", try_parse_dates=True)
total_ds = customers_ds.join(order_ds, on='customer_id')
result = total_ds.select(
    pl.col("customer_unique_id").alias("customer"),
    pl.col("order_id")
).group_by(pl.col("customer")).agg(pl.col("order_id").count().alias("count")).filter(pl.col("count")==1)
"""

"""
--быстрейшие доставки (исключена аномалия с отрицательным временем доставки)
orders_ds = pl.read_csv('olist_orders_dataset.csv', try_parse_dates=True)
customers_ds = pl.read_csv("olist_customers_dataset.csv", try_parse_dates=True)
order_items_ds = pl.read_csv('olist_order_items_dataset.csv', try_parse_dates=True)
sellers_ds = pl.read_csv('olist_sellers_dataset.csv', try_parse_dates=True)
total_ds = orders_ds.join(customers_ds, on='customer_id').join(order_items_ds, on='order_id').join(sellers_ds, on='seller_id')
result = (total_ds.select(
    pl.col("customer_city"),
    pl.col("seller_state"),
    pl.col("order_id"),
    pl.col("order_status"),
    (pl.col("order_delivered_customer_date") - pl.col("order_approved_at")).alias("det"),
    pl.col("order_approved_at"),
    pl.col("order_delivered_customer_date")
).filter(pl.col("order_status") == "delivered", pl.col("order_approved_at").is_not_null(),
         pl.col("order_delivered_customer_date").is_not_null(), pl.col("det")>0).sort("det").limit(10))
"""
"""
--группы товаров которые ни разу не оплачивались картой
products_ds = pl.read_csv("olist_products_dataset.csv", try_parse_dates = True)
order_items_ds = pl.read_csv("olist_order_items_dataset.csv", try_parse_dates = True)
order_payments_ds = pl.read_csv("olist_order_payments_dataset.csv", try_parse_dates=True)
total_ds = products_ds.join(order_items_ds, on = "product_id").join(order_payments_ds, on = "order_id")

result = total_ds.select(
    pl.col("product_category_name"),
    pl.col("order_id"),
    pl.col("payment_type")
).group_by(pl.col("product_category_name")).agg((pl.col("payment_type") == "credit card").sum().alias("card_pay_count")).filter(
    pl.col("card_pay_count") == 0
)
"""
"""
--Среднее значение платежа по штатам (оконной функцией)
sellers_ds = pl.read_csv("olist_sellers_dataset.csv", try_parse_dates=True)
order_items_ds = pl.read_csv("olist_order_items_dataset.csv", try_parse_dates=True)
order_payments_ds = pl.read_csv("olist_order_payments_dataset.csv", try_parse_dates=True)
total_ds = sellers_ds.join(order_items_ds, on = "seller_id").join(order_payments_ds, on = "order_id")
result = total_ds.select(
    pl.col("seller_state"),
    pl.col("payment_value").mean().over(pl.col("seller_state"))
).unique()
print(result)
"""