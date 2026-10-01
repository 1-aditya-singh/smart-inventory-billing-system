from database.connection import get_connection


class InventoryTransaction:

    @staticmethod
    def create(
        product_id,
        transaction_type,
        quantity,
        reference_id=None,
        notes=None
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO inventory_transactions
                    (
                        product_id,
                        transaction_type,
                        quantity,
                        reference_id,
                        notes
                    )
                    VALUES
                    (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        product_id,
                        transaction_type,
                        quantity,
                        reference_id,
                        notes
                    )
                )

                transaction_id = cursor.fetchone()[0]

            connection.commit()

            return transaction_id

        finally:
            connection.close()

    @staticmethod
    def get_by_id(transaction_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        it.id,
                        it.product_id,
                        p.name AS product_name,
                        p.sku,
                        it.transaction_type,
                        it.quantity,
                        it.reference_id,
                        it.notes,
                        it.transaction_date
                    FROM inventory_transactions it
                    INNER JOIN products p
                        ON it.product_id = p.id
                    WHERE it.id = %s;
                    """,
                    (transaction_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_by_product(product_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        it.id,
                        it.product_id,
                        p.name AS product_name,
                        p.sku,
                        it.transaction_type,
                        it.quantity,
                        it.reference_id,
                        it.notes,
                        it.transaction_date
                    FROM inventory_transactions it
                    INNER JOIN products p
                        ON it.product_id = p.id
                    WHERE it.product_id = %s
                    ORDER BY it.transaction_date DESC, it.id DESC;
                    """,
                    (product_id,)
                )

                return cursor.fetchall()

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
                        it.id,
                        it.product_id,
                        p.name AS product_name,
                        p.sku,
                        it.transaction_type,
                        it.quantity,
                        it.reference_id,
                        it.notes,
                        it.transaction_date
                    FROM inventory_transactions it
                    INNER JOIN products p
                        ON it.product_id = p.id
                    ORDER BY it.transaction_date DESC, it.id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_type(transaction_type):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        it.id,
                        it.product_id,
                        p.name AS product_name,
                        p.sku,
                        it.transaction_type,
                        it.quantity,
                        it.reference_id,
                        it.notes,
                        it.transaction_date
                    FROM inventory_transactions it
                    INNER JOIN products p
                        ON it.product_id = p.id
                    WHERE it.transaction_type = %s
                    ORDER BY it.transaction_date DESC, it.id DESC;
                    """,
                    (transaction_type,)
                )

                return cursor.fetchall()

        finally:
            connection.close()