from database.connection import get_connection


class ReportService:

    @staticmethod
    def get_dashboard_summary():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                # ------------------------------------------
                # Sales summary
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        COUNT(*) AS total_sales,
                        COALESCE(SUM(total_amount), 0) AS total_revenue,
                        COALESCE(SUM(discount), 0) AS total_discount,
                        COALESCE(SUM(tax), 0) AS total_tax
                    FROM sales
                    WHERE status = 'Completed';
                    """
                )

                sales_summary = cursor.fetchone()

                # ------------------------------------------
                # Product summary
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        COUNT(*) AS total_products,
                        COALESCE(SUM(quantity), 0) AS total_units
                    FROM products;
                    """
                )

                product_summary = cursor.fetchone()

                # ------------------------------------------
                # Customer summary
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM customers;
                    """
                )

                total_customers = cursor.fetchone()[0]

                # ------------------------------------------
                # Low stock count
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM products
                    WHERE quantity <= reorder_level;
                    """
                )

                low_stock_count = cursor.fetchone()[0]

                # ------------------------------------------
                # Inventory value
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            SUM(quantity * cost_price),
                            0
                        ),
                        COALESCE(
                            SUM(quantity * price),
                            0
                        )
                    FROM products;
                    """
                )

                inventory_value = cursor.fetchone()

                return {
                    "total_sales": sales_summary[0],
                    "total_revenue": sales_summary[1],
                    "total_discount": sales_summary[2],
                    "total_tax": sales_summary[3],
                    "total_products": product_summary[0],
                    "total_units": product_summary[1],
                    "total_customers": total_customers,
                    "low_stock_count": low_stock_count,
                    "inventory_cost_value": inventory_value[0],
                    "inventory_retail_value": inventory_value[1]
                }

        finally:
            connection.close()

    @staticmethod
    def get_total_profit():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            SUM(
                                si.quantity
                                * (
                                    si.unit_price
                                    - p.cost_price
                                )
                            ),
                            0
                        ) AS total_profit
                    FROM sale_items si
                    INNER JOIN sales s
                        ON si.sale_id = s.id
                    INNER JOIN products p
                        ON si.product_id = p.id
                    WHERE s.status = 'Completed';
                    """
                )

                return cursor.fetchone()[0]

        finally:
            connection.close()

    @staticmethod
    def get_top_selling_products(limit=10):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.sku,
                        SUM(si.quantity) AS units_sold,
                        SUM(si.subtotal) AS revenue
                    FROM sale_items si
                    INNER JOIN sales s
                        ON si.sale_id = s.id
                    INNER JOIN products p
                        ON si.product_id = p.id
                    WHERE s.status = 'Completed'
                    GROUP BY
                        p.id,
                        p.name,
                        p.sku
                    ORDER BY units_sold DESC
                    LIMIT %s;
                    """,
                    (limit,)
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_payment_method():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        payment_method,
                        COUNT(*) AS sales_count,
                        COALESCE(
                            SUM(total_amount),
                            0
                        ) AS revenue
                    FROM sales
                    WHERE status = 'Completed'
                    GROUP BY payment_method
                    ORDER BY revenue DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_date():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        sale_date,
                        COUNT(*) AS sales_count,
                        COALESCE(
                            SUM(total_amount),
                            0
                        ) AS revenue
                    FROM sales
                    WHERE status = 'Completed'
                    GROUP BY sale_date
                    ORDER BY sale_date;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_month():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        DATE_TRUNC(
                            'month',
                            sale_date
                        ) AS month,
                        COUNT(*) AS sales_count,
                        COALESCE(
                            SUM(total_amount),
                            0
                        ) AS revenue
                    FROM sales
                    WHERE status = 'Completed'
                    GROUP BY month
                    ORDER BY month;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_category():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        c.name AS category_name,
                        SUM(si.quantity) AS units_sold,
                        COALESCE(
                            SUM(si.subtotal),
                            0
                        ) AS revenue
                    FROM sale_items si
                    INNER JOIN sales s
                        ON si.sale_id = s.id
                    INNER JOIN products p
                        ON si.product_id = p.id
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    WHERE s.status = 'Completed'
                    GROUP BY c.name
                    ORDER BY revenue DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_low_stock_report():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.sku,
                        c.name AS category_name,
                        p.quantity,
                        p.reorder_level,
                        p.cost_price,
                        p.price
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    WHERE p.quantity <= p.reorder_level
                    ORDER BY
                        p.quantity ASC,
                        p.name;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_customer_sales():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        c.id,
                        c.name,
                        COUNT(s.id) AS total_orders,
                        COALESCE(
                            SUM(s.total_amount),
                            0
                        ) AS total_spent
                    FROM customers c
                    LEFT JOIN sales s
                        ON c.id = s.customer_id
                        AND s.status = 'Completed'
                    GROUP BY
                        c.id,
                        c.name
                    ORDER BY total_spent DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()