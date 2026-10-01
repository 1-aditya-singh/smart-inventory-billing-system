from database.connection import get_connection


class Product:

    @staticmethod
    def create(
        name,
        description,
        category_id,
        supplier_id,
        sku,
        price,
        cost_price,
        quantity=0,
        reorder_level=5
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products
                    (
                        name,
                        description,
                        category_id,
                        supplier_id,
                        sku,
                        price,
                        cost_price,
                        quantity,
                        reorder_level
                    )
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        name,
                        description,
                        category_id,
                        supplier_id,
                        sku,
                        price,
                        cost_price,
                        quantity,
                        reorder_level
                    )
                )

                product_id = cursor.fetchone()[0]

            connection.commit()

            return product_id

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
                        p.id,
                        p.name,
                        p.description,
                        p.category_id,
                        c.name AS category_name,
                        p.supplier_id,
                        s.name AS supplier_name,
                        p.sku,
                        p.price,
                        p.cost_price,
                        p.quantity,
                        p.reorder_level,
                        p.created_at,
                        p.updated_at
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    LEFT JOIN suppliers s
                        ON p.supplier_id = s.id
                    ORDER BY p.id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_id(product_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.description,
                        p.category_id,
                        c.name AS category_name,
                        p.supplier_id,
                        s.name AS supplier_name,
                        p.sku,
                        p.price,
                        p.cost_price,
                        p.quantity,
                        p.reorder_level,
                        p.created_at,
                        p.updated_at
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    LEFT JOIN suppliers s
                        ON p.supplier_id = s.id
                    WHERE p.id = %s;
                    """,
                    (product_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_by_sku(sku):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.description,
                        p.category_id,
                        c.name AS category_name,
                        p.supplier_id,
                        s.name AS supplier_name,
                        p.sku,
                        p.price,
                        p.cost_price,
                        p.quantity,
                        p.reorder_level
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    LEFT JOIN suppliers s
                        ON p.supplier_id = s.id
                    WHERE p.sku = %s;
                    """,
                    (sku,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def search(search_term):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                search_pattern = f"%{search_term}%"

                cursor.execute(
                    """
                    SELECT
                        p.id,
                        p.name,
                        p.sku,
                        c.name AS category_name,
                        s.name AS supplier_name,
                        p.price,
                        p.quantity,
                        p.reorder_level
                    FROM products p
                    LEFT JOIN categories c
                        ON p.category_id = c.id
                    LEFT JOIN suppliers s
                        ON p.supplier_id = s.id
                    WHERE
                        p.name ILIKE %s
                        OR p.sku ILIKE %s
                    ORDER BY p.name;
                    """,
                    (search_pattern, search_pattern)
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_low_stock():
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
    def update(
        product_id,
        name,
        description,
        category_id,
        supplier_id,
        sku,
        price,
        cost_price,
        quantity,
        reorder_level
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET
                        name = %s,
                        description = %s,
                        category_id = %s,
                        supplier_id = %s,
                        sku = %s,
                        price = %s,
                        cost_price = %s,
                        quantity = %s,
                        reorder_level = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s;
                    """,
                    (
                        name,
                        description,
                        category_id,
                        supplier_id,
                        sku,
                        price,
                        cost_price,
                        quantity,
                        reorder_level,
                        product_id
                    )
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def update_stock(product_id, quantity_change):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET
                        quantity = quantity + %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE
                        id = %s
                        AND quantity + %s >= 0;
                    """,
                    (
                        quantity_change,
                        product_id,
                        quantity_change
                    )
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(product_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM products
                    WHERE id = %s;
                    """,
                    (product_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()