from database.connection import get_connection


class SaleItem:

    @staticmethod
    def create(
        sale_id,
        product_id,
        quantity,
        unit_price,
        subtotal
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO sale_items
                    (
                        sale_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        sale_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                )

                item_id = cursor.fetchone()[0]

            connection.commit()

            return item_id

        finally:
            connection.close()

    @staticmethod
    def get_by_id(item_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        si.id,
                        si.sale_id,
                        si.product_id,
                        p.name AS product_name,
                        p.sku,
                        si.quantity,
                        si.unit_price,
                        si.subtotal
                    FROM sale_items si
                    INNER JOIN products p
                        ON si.product_id = p.id
                    WHERE si.id = %s;
                    """,
                    (item_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_by_sale(sale_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        si.id,
                        si.sale_id,
                        si.product_id,
                        p.name AS product_name,
                        p.sku,
                        si.quantity,
                        si.unit_price,
                        si.subtotal
                    FROM sale_items si
                    INNER JOIN products p
                        ON si.product_id = p.id
                    WHERE si.sale_id = %s
                    ORDER BY si.id;
                    """,
                    (sale_id,)
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def update(
        item_id,
        quantity,
        unit_price,
        subtotal
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE sale_items
                    SET
                        quantity = %s,
                        unit_price = %s,
                        subtotal = %s
                    WHERE id = %s;
                    """,
                    (
                        quantity,
                        unit_price,
                        subtotal,
                        item_id
                    )
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(item_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM sale_items
                    WHERE id = %s;
                    """,
                    (item_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()

    @staticmethod
    def delete_by_sale(sale_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM sale_items
                    WHERE sale_id = %s;
                    """,
                    (sale_id,)
                )

                deleted_count = cursor.rowcount

            connection.commit()

            return deleted_count

        finally:
            connection.close()

    @staticmethod
    def get_product_sales(product_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        si.id,
                        si.sale_id,
                        s.invoice_number,
                        s.sale_date,
                        si.quantity,
                        si.unit_price,
                        si.subtotal
                    FROM sale_items si
                    INNER JOIN sales s
                        ON si.sale_id = s.id
                    WHERE si.product_id = %s
                    ORDER BY s.sale_date DESC, s.id DESC;
                    """,
                    (product_id,)
                )

                return cursor.fetchall()

        finally:
            connection.close()