from database.connection import get_connection


class Customer:

    @staticmethod
    def create(name, contact, email=None, address=None):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers
                    (name, contact, email, address)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (name, contact, email, address)
                )

                customer_id = cursor.fetchone()[0]

            connection.commit()

            return customer_id

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
                        id,
                        name,
                        contact,
                        email,
                        address,
                        created_at
                    FROM customers
                    ORDER BY id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_id(customer_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        contact,
                        email,
                        address,
                        created_at
                    FROM customers
                    WHERE id = %s;
                    """,
                    (customer_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def update(customer_id, name, contact, email=None, address=None):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE customers
                    SET
                        name = %s,
                        contact = %s,
                        email = %s,
                        address = %s
                    WHERE id = %s;
                    """,
                    (name, contact, email, address, customer_id)
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(customer_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM customers
                    WHERE id = %s;
                    """,
                    (customer_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()