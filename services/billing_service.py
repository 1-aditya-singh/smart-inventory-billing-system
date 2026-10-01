from database.connection import get_connection


class BillingService:

    TAX_RATE = 0.05

    @staticmethod
    def generate_invoice_number(cursor):
        cursor.execute(
            """
            SELECT COUNT(*) + 1
            FROM sales;
            """
        )

        next_number = cursor.fetchone()[0]

        return f"INV-{next_number:05d}"

    @staticmethod
    def calculate_totals(items, discount=0):
        subtotal = 0

        for item in items:
            quantity = item["quantity"]
            unit_price = item["unit_price"]

            if quantity <= 0:
                raise ValueError(
                    "Product quantity must be greater than 0."
                )

            if unit_price < 0:
                raise ValueError(
                    "Product price cannot be negative."
                )

            subtotal += quantity * unit_price

        if discount < 0:
            raise ValueError(
                "Discount cannot be negative."
            )

        if discount > subtotal:
            raise ValueError(
                "Discount cannot be greater than subtotal."
            )

        taxable_amount = subtotal - discount

        tax = taxable_amount * BillingService.TAX_RATE

        total_amount = taxable_amount + tax

        return {
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "discount": round(discount, 2),
            "total_amount": round(total_amount, 2)
        }

    @staticmethod
    def create_invoice(
        customer_id,
        items,
        discount=0,
        payment_method="Cash"
    ):
        if not items:
            raise ValueError(
                "Invoice must contain at least one product."
            )

        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                # ------------------------------------------
                # Validate customer
                # ------------------------------------------

                if customer_id is not None:
                    cursor.execute(
                        """
                        SELECT id
                        FROM customers
                        WHERE id = %s;
                        """,
                        (customer_id,)
                    )

                    customer = cursor.fetchone()

                    if customer is None:
                        raise ValueError(
                            "Customer not found."
                        )

                # ------------------------------------------
                # Validate products and stock
                # ------------------------------------------

                validated_items = []

                for item in items:

                    product_id = item["product_id"]
                    requested_quantity = item["quantity"]

                    if requested_quantity <= 0:
                        raise ValueError(
                            "Product quantity must be greater than 0."
                        )

                    cursor.execute(
                        """
                        SELECT
                            id,
                            name,
                            sku,
                            price,
                            quantity
                        FROM products
                        WHERE id = %s
                        FOR UPDATE;
                        """,
                        (product_id,)
                    )

                    product = cursor.fetchone()

                    if product is None:
                        raise ValueError(
                            f"Product ID {product_id} not found."
                        )

                    (
                        product_id,
                        product_name,
                        sku,
                        price,
                        available_quantity
                    ) = product

                    if available_quantity < requested_quantity:
                        raise ValueError(
                            f"Insufficient stock for "
                            f"{product_name}. "
                            f"Available: {available_quantity}, "
                            f"Requested: {requested_quantity}"
                        )

                    validated_items.append(
                        {
                            "product_id": product_id,
                            "product_name": product_name,
                            "sku": sku,
                            "quantity": requested_quantity,
                            "unit_price": float(price)
                        }
                    )

                # ------------------------------------------
                # Calculate totals
                # ------------------------------------------

                totals = BillingService.calculate_totals(
                    validated_items,
                    discount
                )

                # ------------------------------------------
                # Generate invoice number
                # ------------------------------------------

                invoice_number = (
                    BillingService.generate_invoice_number(
                        cursor
                    )
                )

                # ------------------------------------------
                # Create sale
                # ------------------------------------------

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
                        totals["subtotal"],
                        totals["tax"],
                        totals["discount"],
                        totals["total_amount"],
                        payment_method,
                        "Completed"
                    )
                )

                sale_id = cursor.fetchone()[0]

                # ------------------------------------------
                # Create sale items
                # ------------------------------------------

                for item in validated_items:

                    item_subtotal = (
                        item["quantity"]
                        * item["unit_price"]
                    )

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
                        (%s, %s, %s, %s, %s);
                        """,
                        (
                            sale_id,
                            item["product_id"],
                            item["quantity"],
                            item["unit_price"],
                            round(item_subtotal, 2)
                        )
                    )

                    # --------------------------------------
                    # Deduct stock
                    # --------------------------------------

                    cursor.execute(
                        """
                        UPDATE products
                        SET
                            quantity = quantity - %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE
                            id = %s
                            AND quantity >= %s;
                        """,
                        (
                            item["quantity"],
                            item["product_id"],
                            item["quantity"]
                        )
                    )

                    if cursor.rowcount == 0:
                        raise ValueError(
                            f"Stock update failed for "
                            f"{item['product_name']}."
                        )

                    # --------------------------------------
                    # Record inventory transaction
                    # --------------------------------------

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
                        (%s, %s, %s, %s, %s);
                        """,
                        (
                            item["product_id"],
                            "SALE",
                            item["quantity"],
                            sale_id,
                            f"Sale {invoice_number}"
                        )
                    )

            connection.commit()

            return {
                "sale_id": sale_id,
                "invoice_number": invoice_number,
                **totals
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_invoice(sale_id):
        connection = get_connection()

        
        with connection.cursor() as cursor:

            # ------------------------------------------
            # Sale information
            # ------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        s.id,
                        s.invoice_number,
                        s.sale_date,
                        s.customer_id,
                        c.name AS customer_name,
                        c.contact AS customer_contact,
                        s.subtotal,
                        s.tax,
                        s.discount,
                        s.total_amount,
                        s.payment_method,
                        s.status
                    FROM sales s
                    LEFT JOIN customers c
                        ON s.customer_id = c.id
                    WHERE s.id = %s;
                    """,
                    (sale_id,)
                )

                sale = cursor.fetchone()

                if sale is None:
                    return None

                # ------------------------------------------
                # Sale items
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        si.id,
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

                items = cursor.fetchall()

                return {
                    "sale": sale,
                    "items": items
                }