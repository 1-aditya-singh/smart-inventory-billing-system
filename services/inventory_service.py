from database.connection import get_connection


class InventoryService:

    @staticmethod
    def stock_in(
        product_id,
        quantity,
        notes=None,
        reference_id=None
    ):
        if quantity <= 0:
            raise ValueError("Stock-in quantity must be greater than 0.")

        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                # ------------------------------------------
                # Update product stock
                # ------------------------------------------

                cursor.execute(
                    """
                    UPDATE products
                    SET
                        quantity = quantity + %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                    """,
                    (quantity, product_id)
                )

                if cursor.rowcount == 0:
                    raise ValueError("Product not found.")

                # ------------------------------------------
                # Record inventory transaction
                # ------------------------------------------

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
                        "STOCK_IN",
                        quantity,
                        reference_id,
                        notes
                    )
                )

                transaction_id = cursor.fetchone()[0]

            connection.commit()

            return transaction_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def stock_out(
        product_id,
        quantity,
        notes=None,
        reference_id=None
    ):
        if quantity <= 0:
            raise ValueError("Stock-out quantity must be greater than 0.")

        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                # ------------------------------------------
                # Check available stock
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT quantity
                    FROM products
                    WHERE id = %s
                    FOR UPDATE;
                    """,
                    (product_id,)
                )

                product = cursor.fetchone()

                if product is None:
                    raise ValueError("Product not found.")

                current_stock = product[0]

                if current_stock < quantity:
                    raise ValueError(
                        f"Insufficient stock. "
                        f"Available: {current_stock}, "
                        f"Requested: {quantity}"
                    )

                # ------------------------------------------
                # Deduct stock
                # ------------------------------------------

                cursor.execute(
                    """
                    UPDATE products
                    SET
                        quantity = quantity - %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                    """,
                    (quantity, product_id)
                )

                # ------------------------------------------
                # Record inventory transaction
                # ------------------------------------------

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
                        "STOCK_OUT",
                        quantity,
                        reference_id,
                        notes
                    )
                )

                transaction_id = cursor.fetchone()[0]

            connection.commit()

            return transaction_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def adjust_stock(
        product_id,
        new_quantity,
        notes=None
    ):
        if new_quantity < 0:
            raise ValueError(
                "Stock quantity cannot be negative."
            )

        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                # ------------------------------------------
                # Get current stock
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT quantity
                    FROM products
                    WHERE id = %s
                    FOR UPDATE;
                    """,
                    (product_id,)
                )

                product = cursor.fetchone()

                if product is None:
                    raise ValueError("Product not found.")

                old_quantity = product[0]

                difference = new_quantity - old_quantity

                # ------------------------------------------
                # Update stock
                # ------------------------------------------

                cursor.execute(
                    """
                    UPDATE products
                    SET
                        quantity = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                    """,
                    (new_quantity, product_id)
                )

                # ------------------------------------------
                # Record adjustment
                # ------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO inventory_transactions
                    (
                        product_id,
                        transaction_type,
                        quantity,
                        notes
                    )
                    VALUES
                    (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        product_id,
                        "ADJUSTMENT",
                        difference,
                        notes
                    )
                )

                transaction_id = cursor.fetchone()[0]

            connection.commit()

            return transaction_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_stock(product_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        sku,
                        quantity,
                        reorder_level
                    FROM products
                    WHERE id = %s;
                    """,
                    (product_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_low_stock_products():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.sku,
                        p.quantity,
                        p.reorder_level,
                        c.name AS category_name
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    WHERE p.quantity <= p.reorder_level
                    ORDER BY p.quantity ASC, p.name;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_inventory_value():
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            SUM(quantity * cost_price),
                            0
                        ) AS inventory_cost_value,
                        COALESCE(
                            SUM(quantity * price),
                            0
                        ) AS inventory_retail_value
                    FROM products;
                    """
                )

                return cursor.fetchone()

        finally:
            connection.close()