-- Помесячная динамика заказов:
SELECT strftime('%m', order_purchase_timestamp) AS month, COUNT(order_id) as count FROM olist_orders_dataset GROUP BY month;
-- Топ-10 категорий по объему продаж
SELECT product_category_name, SUM(price) AS revenue FROM olist_products_dataset
INNER JOIN olist_order_items_dataset ON olist_products_dataset.product_id = olist_order_items_dataset.product_id GROUP BY product_category_name ORDER BY revenue DESC
LIMIT 10;
-- География клиентов с высокой оценкой:
SELECT customer_city, COUNT(customer_city) as count_5 FROM olist_customers_dataset INNER JOIN olist_orders_dataset ON olist_customers_dataset.customer_id = olist_orders_dataset.customer_id
INNER JOIN olist_order_reviews_dataset ON olist_orders_dataset.order_id = olist_order_reviews_dataset.order_id WHERE review_score = 5 GROUP BY customer_city ORDER BY count_5 DESC LIMIT 5;
-- Среднее время доставки по штатам
SELECT 
    c.customer_state,
    ROUND(AVG(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_approved_at)), 1) AS avg_delivery_days
FROM olist_orders_dataset o
INNER JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' 
  AND o.order_approved_at IS NOT NULL 
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days DESC;
-- Клиенты без повторных покупок:
SELECT customer_unique_id AS customer FROM olist_customers_dataset INNER JOIN olist_orders_dataset ON 
olist_customers_dataset.customer_id = olist_orders_dataset.customer_id GROUP BY customer_unique_id 
HAVING COUNT(order_id) = 1;
-- Анализ самых быстрых доставок
SELECT (julianday(order_delivered_customer_date) - julianday(order_approved_at)) as speed, order_id, customer_city, seller_state FROM olist_orders_dataset 
INNER JOIN olist_order_items_dataset ON olist_orders_dataset.order_id = olist_order_items_dataset.order_id 
INNER JOIN olist_sellers_dataset ON olist_order_items_dataset.seller_id = olist_sellers_dataset.seller_id 
INNER JOIN olist_customers_dataset ON olist_orders_dataset.customer_id = olist_customers_dataset.customer_id 
WHERE order_approved_at IS NOT NULL AND order_delivered_customer_date IS NOT NULL AND order_status = "delivered"
ORDER BY speed ASC LIMIT 10;
SELECT product_category_name
FROM olist_products_dataset 
INNER JOIN olist_order_items_dataset ON olist_products_dataset.product_id = olist_order_items_dataset.product_id
INNER JOIN olist_order_payments_dataset ON olist_order_items_dataset.order_id = olist_order_payments_dataset.order_id 
WHERE olist_order_items_dataset.order_id NOT IN (
    SELECT order_id FROM olist_order_payments_dataset 
    WHERE payment_type = "credit card" AND order_id IS NOT NULL
);
SELECT DISTINCT seller_state, AVG(payment_value) OVER(PARTITION BY seller_state) AS avg_payment_in_state FROM olist_sellers_dataset 
INNER JOIN olist_order_items_dataset ON olist_sellers_dataset.seller_id = olist_order_items_dataset.seller_id 
INNER JOIN olist_order_payments_dataset ON olist_order_items_dataset.order_id = olist_order_payments_dataset.order_id;
SELECT ROW_NUMBER() OVER(PARTITION BY seller_state ORDER BY SUM(payment_value) DESC) as state_rank, seller_state, olist_order_items_dataset.seller_id, SUM(payment_value) as total_revenue
FROM olist_sellers_dataset INNER JOIN olist_order_items_dataset ON olist_sellers_dataset.seller_id = olist_order_items_dataset.seller_id 
INNER JOIN olist_order_payments_dataset ON olist_order_items_dataset.order_id = olist_order_payments_dataset.order_id GROUP BY olist_order_items_dataset.seller_id , seller_state 
ORDER BY seller_state;