from database.connection import get_connection


class Supplier:

    @staticmethod
    def create(name, contact, email=None, address=None):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO suppliers
                    (name, contact, email, address)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (name, contact, email, address)
                )

                supplier_id = cursor.fetchone()[0]

            connection.commit()

            return supplier_id

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
                    FROM suppliers
                    ORDER BY id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_id(supplier_id):
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
                    FROM suppliers
                    WHERE id = %s;
                    """,
                    (supplier_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def update(
        supplier_id,
        name,
        contact,
        email=None,
        address=None
    ):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE suppliers
                    SET
                        name = %s,
                        contact = %s,
                        email = %s,
                        address = %s
                    WHERE id = %s;
                    """,
                    (
                        name,
                        contact,
                        email,
                        address,
                        supplier_id
                    )
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(supplier_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM suppliers
                    WHERE id = %s;
                    """,
                    (supplier_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()