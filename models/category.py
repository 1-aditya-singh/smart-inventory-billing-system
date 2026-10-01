from database.connection import get_connection


class Category:

    @staticmethod
    def create(name, description=None):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO categories
                    (name, description)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (name, description)
                )

                category_id = cursor.fetchone()[0]

            connection.commit()

            return category_id

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
                        description,
                        created_at
                    FROM categories
                    ORDER BY id DESC;
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_by_id(category_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        description,
                        created_at
                    FROM categories
                    WHERE id = %s;
                    """,
                    (category_id,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def update(category_id, name, description=None):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE categories
                    SET
                        name = %s,
                        description = %s
                    WHERE id = %s;
                    """,
                    (name, description, category_id)
                )

                updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    @staticmethod
    def delete(category_id):
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM categories
                    WHERE id = %s;
                    """,
                    (category_id,)
                )

                deleted = cursor.rowcount > 0

            connection.commit()

            return deleted

        finally:
            connection.close()