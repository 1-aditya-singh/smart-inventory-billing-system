from database.connection import get_connection


class Sale:

    @staticmethod
    def create(
        customer_id,
        invoice_number,
        subtotal,
        tax=0,
        discount=0,
        total_amount=0,
        payment_method="Cash",
        status="Completed"
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO sales
                    (
                        customer_id,
                        invoice_number,
                        subtotal,
                        tax,
                        discount,
                        total_amount,
                        payment_method,
                        status
                    )
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        customer_id,
                        invoice_number,
                        subtotal,
                        tax,
                        discount,
                        total_amount,
                        payment_method,
                        status
                    )
                )

                sale_id = cursor.fetchone()[0]

            connection.commit()

            return sale_id

        finally:
            connection.close()

    @staticmethod
    def get_all():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        s.id,
                        s.invoice_number,
                        s.sale_date,
                        s.customer_id,
                        c.name AS customer_name,
                        s.subtotal,
                        s.tax,
                        s.discount,
                        s.total_amount,
                        s.payment_method,
                        s.status,
                        s.created_at
                    FROM sales s
                    LEFT JOIN customers c
                        ON s.customer_id = c.id
                    ORDER BY s.id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_id(sale_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        s.id,
                        s.invoice_number,
                        s.sale_date,
                        s.customer_id,
                        c.name AS customer_name,
                        s.subtotal,
                        s.tax,
                        s.discount,
                        s.total_amount,
                        s.payment_method,
                        s.status,
                        s.created_at
                    FROM sales s
                    LEFT JOIN customers c
                        ON s.customer_id = c.id
                    WHERE s.id = %s;
                    """,
                    (sale_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_by_invoice(invoice_number):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        s.id,
                        s.invoice_number,
                        s.sale_date,
                        s.customer_id,
                        c.name AS customer_name,
                        s.subtotal,
                        s.tax,
                        s.discount,
                        s.total_amount,
                        s.payment_method,
                        s.status
                    FROM sales s
                    LEFT JOIN customers c
                        ON s.customer_id = c.id
                    WHERE s.invoice_number = %s;
                    """,
                    (invoice_number,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def update(
        sale_id,
        customer_id,
        subtotal,
        tax,
        discount,
        total_amount,
        payment_method,
        status
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE sales
                    SET
                        customer_id = %s,
                        subtotal = %s,
                        tax = %s,
                        discount = %s,
                        total_amount = %s,
                        payment_method = %s,
                        status = %s
                    WHERE id = %s;
                    """,
                    (
                        customer_id,
                        subtotal,
                        tax,
                        discount,
                        total_amount,
                        payment_method,
                        status,
                        sale_id
                    )
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(sale_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM sales
                    WHERE id = %s;
                    """,
                    (sale_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_customer(customer_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        invoice_number,
                        sale_date,
                        subtotal,
                        tax,
                        discount,
                        total_amount,
                        payment_method,
                        status
                    FROM sales
                    WHERE customer_id = %s
                    ORDER BY sale_date DESC, id DESC;
                    """,
                    (customer_id,)
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_sales_by_date_range(start_date, end_date):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        invoice_number,
                        sale_date,
                        customer_id,
                        subtotal,
                        tax,
                        discount,
                        total_amount,
                        payment_method,
                        status
                    FROM sales
                    WHERE sale_date BETWEEN %s AND %s
                    ORDER BY sale_date DESC, id DESC;
                    """,
                    (start_date, end_date)
                )

                return cursor.fetchall()

        finally:
            connection.close()